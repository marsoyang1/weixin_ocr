# -*- coding: utf-8 -*-
'''
本项目采用科大讯飞提供的:通用文字识别API识别微信对话截图内容,接口文档地址:https://www.xfyun.cn/doc/words/universal_character_recognition/API.html
1、通用文字识别,图像数据base64编码后大小不得超过10M
2、appid、apiSecret、apiKey请到讯飞开放平台控制台获取并填写到config文件
3、支持中英文,支持手写和印刷文字。
4、在倾斜文字上效果有提升,同时支持部分生僻字的识别
'''

from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
import json
import requests
import cv2
import numpy as np
from urllib.parse import urlencode


class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg

class XunFeiSDK:
    def __init__(self, APPId, APISecret, APIKey):
        self.APPId = APPId
        self.APISecret = APISecret
        self.APIKey = APIKey

    def ocr_request(self,image):
        # Encode the new image in the appropriate format
        image_encode = cv2.imencode('.jpg',image)[1]
        # Convert the encoded image back to bytes
        imageBytes = np.array(image_encode).tostring() 
        url = 'https://api.xf-yun.com/v1/private/sf8e6aca1'

        body = {
            "header": {
                "app_id": self.APPId,
                "status": 3
            },
            "parameter": {
                "sf8e6aca1": {
                    "category": "ch_en_public_cloud",
                    "result": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "sf8e6aca1_data_1": {
                    "encoding": "jpg",
                    "image": str(base64.b64encode(imageBytes), 'UTF-8'),
                    "status": 3
                }
            }
        }
        
        request_url = self.assemble_ws_auth_url(url, "POST", self.APIKey, self.APISecret)

        headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'app_id': self.APPId}
        
        response = requests.post(request_url, data=json.dumps(body), headers=headers)
        tempResult = json.loads(response.content.decode())

        finalResult = base64.b64decode(tempResult['payload']['result']['text']).decode()
        finalResult = finalResult.replace(" ", "").replace("\n", "").replace("\t", "").strip()
        return finalResult

    def parse_url(self,requset_url):
        stidx = requset_url.index("://")
        host = requset_url[stidx + 3:]
        edidx = host.index("/")
        if edidx <= 0:
            raise AssembleHeaderException("invalid request url:" + requset_url)
        path = host[edidx:]
        host = host[:edidx]
        return host, path


    # build websocket auth request url
    def assemble_ws_auth_url(self,requset_url, method="POST", api_key="", api_secret=""):
        request_info = self.parse_url(requset_url)
        host = request_info[0]
        path = request_info[1]
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        
        # date = "Thu, 12 Dec 2019 01:57:27 GMT"
        signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
        
        signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            api_key, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        
        values = {
            "host": host,
            "date": date,
            "authorization": authorization
        }

        return requset_url + "?" + urlencode(values)