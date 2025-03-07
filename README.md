# weixin_ocr <img src="https://github.com/acheong08/ChatGPT/blob/main/logo.png?raw=true" width="7%"></img>

[![PyPi](https://img.shields.io/pypi/v/revChatGPT.svg)](https://pypi.python.org/pypi/revChatGPT)
[![Downloads](https://static.pepy.tech/badge/revchatgpt)](https://pypi.python.org/pypi/revChatGPT)

本项目封装科大讯飞接口实现微信聊天截图文字的识别，识别准确率高达99%，并且可以分清楚对话文本来自对方还是自己.


## 安装准备
`pip3 install -r requestments.txt`


## 使用方法
```
1.配置微信截图图片地址:filename = "image/5e5eb526-90e7-4915-8e00-b363f8bce2b2.jpg"
2.python3 -m image_ocr.py
3.ocr识别文本结果输出到result.txt
```

## 效果展示
微信截图：

[![微信截图](https://i.postimg.cc/gjjyvmxm/5e5eb526-90e7-4915-8e00-b363f8bce2b2.jpg)](https://postimg.cc/LgdZSdkb)

识别结果：
```
好友:400自提得行不
自己:太低了哦
好友:我还要去买个显示器。唉。
自己:显示器便宜
自己:如果要大,就用电视
自己:我都是用的电视
好友:不合适的嘛。我要玩梦幻西游搬砖
自己:噢噢
好友:怎么样。400自提行不
自己:在高点呢
```

## 注意
如何额度用完或到期了，请自行购买讯飞服务，购买路径如下图：
[![购买路径截图](https://i.postimg.cc/tJyd6VPt/1741337654058.png)](https://postimg.cc/jwgJ02ML)
先创建应用，然后找到【文字识别】-【通用文字识别】，点击购买服务，选择刚刚创建的应用名称，一般有免费体验包，或者直接付费购买

## 联系作者反馈问题
[![微信二维码](https://i.postimg.cc/3J0TrGtJ/4aaa650a-febf-4d70-9059-b836b4478cf6.jpg)](https://postimg.cc/Mvw4dnkh)

# 说明

这是一个私人项目，依赖于科大讯飞云提供的OCR识别接口, [`文档地址`](https://www.xfyun.cn/doc/words/universal_character_recognition/API.html "科大讯飞云") ，要大量商业使用，请自行前往科大讯飞云购买接口服务。

# 感谢

- [科大讯飞](https://www.xfyun.cn/) - 感谢大气的它提供免费10万次调用API，因此本人也把自己的KEY无私奉献给大家调用，用完后请自行注册切换为自己的。
