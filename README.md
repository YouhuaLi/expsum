# 简介
a python practice of https://www.johndcook.com/blog/2017/10/07/exponential-sums-make-pretty-pictures/

用非常简单的python代码绘制好看的图形。原理参见：https://www.johndcook.com/blog/2017/10/07/exponential-sums-make-pretty-pictures/

# python 环境
python 3.x

# 本地测试
```bash
git clone https://github.com/YouhuaLi/expsum.git
cd expsum
pip install -r requirements.txt
python application.py
```
然后打开 http://127.0.0.1:5000/ ，可在页面中看到这种图形：

![expsum-example](https://www.johndcook.com/expsum01.png)

## 用s3存储
编辑application.py，将
```
mode = "local"
```
改成
```
mode = "s3"
```
然后用AWS beanstalk部署到AWS上，可实现在线访问。
