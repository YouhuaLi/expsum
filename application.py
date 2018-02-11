import io
from flask import Flask, request
from flask import render_template
from numpy import array, pi, exp
import boto3
import botocore
import matplotlib
matplotlib.use('agg', warn=False, force=True)
import matplotlib.pyplot as plt

# EB looks for an 'application' callable by default.
application = Flask(__name__)
# --- SECRET_KEY is defined to use session object ---
# application.config['SECRET_KEY']='development key'

mode = "local"

@application.route('/', methods=['GET'])
def expsum_main():
    if request.args.get('date', None):
        date = request.args['date']
    else:
        date = "1980-12-01"

    date = date[2:] # remove 'centry' information. Date will be like 80-12-01

    generateimage(date, mode)

    image_file_name = date + '.png'
    return render_template('imageframe.html', imagefile=image_file_name)


def image_exists_in_s3(date):
    s3 = boto3.resource('s3')

    try:
        s3.Object('expsum', date+ ".png").load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            return False
        else:
            # Something else has gone wrong. need better error handle here
            return False

    # The object exists.
    return True


@application.route('/expsum')
def expsum_birthday():
    return 'Hello, expsum for birthday!'


def generateimage(date, mode):
    year = int(date[0:2])
    month = int(date[3:5])
    day = int(date[6:8])

    if year == 0: #when year is 1900 or 2000, we use "100" as year number, instead of "0"
        year = 100

    N = 12000

    def f(n):
        return n/float(month) + n**2/float(day) + n**3/float(year)

    z = array([exp(2*pi*1j*f(n)) for n in range(3, N+3)])
    z = z.cumsum()

    plt.axes().set_aspect(1)
    plt.plot(z.real, z.imag, color='#333399')

    if mode == "s3":
        img_data = io.BytesIO()
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        s3 = boto3.resource('s3')
        bucket = s3.Bucket("expsum")
        bucket.put_object(Body=img_data, ContentType='image/png',
                          Key=date + ".png")
        img_acl = s3.ObjectAcl('expsum', date + ".png")
        img_acl.put(ACL='public-read')
    else:
        plt.savefig('static/' + date + ".png")

    plt.cla()

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
