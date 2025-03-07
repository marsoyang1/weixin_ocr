import json
import math
import re

import cv2
import numpy as np

from universal_character_recognition import XunFeiSDK

'''
Analyse the result lines of XunFei's OCR API
'''
def msg_type(line_dict, image):
    if len(line_dict) == 6:
        inner_lines = line_dict.get('words')
        words=''
        for line in inner_lines:
            words += line.get('content')+','
        words = words[:-1]
        print(words)
        x = inner_lines[0].get('coord')[0]['x']
        y = inner_lines[0].get('coord')[0]['y']
        y3 = inner_lines[0].get('coord')[3]['y']
        y = y + int((y3 - y)/2)#计算首个文字的正中心起始位置，确保后续计算对话框背景颜色更准确
        color = image[y][x]
        
        print((x,y), color)
        return words,(x, y),color
    else:
        return None,(None,None),None

'''
The OCR accurate ratio is best when the image of width equal 541,through the big test
'''
def image_resize(image):
    #image = cv2.imdecode(np.frombuffer(imageBytes, np.uint8), cv2.IMREAD_COLOR)
    (h,w) = image.shape[:2]
    WIDTH = 541
    # Calculate the ratio of height and width
    r = WIDTH / float(w)
    # Create a dimension with the calculated width and height
    dim = (WIDTH, int(h * r))
    # Resize the image
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    return image

'''
If the height of the image is greater than or equal to 3000, the image will be split to images with width of 500 and height 2000
'''
def image_split(imageBytes):
    # Read image from imageBytes
    image = cv2.imdecode(np.frombuffer(imageBytes, np.uint8), cv2.IMREAD_COLOR)
    (h, w) = image.shape[:2]

    sub_images = []
    # If height is greater than or equal to 2000
    if h >= 2000:
        # Split image into multiple images
        num = int(math.ceil(h/2000))
        height = int(h/num)
        
        for i in range(num):
            # Calculate the dimensions of the sub-image
            startY = i*height
            endY = (i+1)*height
            width = w
            dim = (width, endY - startY)
            # Double check that the dimensions are within bounds
            if dim[0]<=w and dim[1]<=h:
                # Resize the sub-image
                sub_image = cv2.resize(image[startY:endY, 0:w], dim, interpolation=cv2.INTER_AREA)
                # Save the sub-image
                #cv2.imwrite('test_{}.png'.format(i),sub_image)
                # Add the sub-image to the list
                sub_images.append(sub_image)
    else:
        sub_images.append(image)
    return sub_images

'''read XunFei config'''
def get_config_json(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        config = json.load(f)
    return config

if __name__ == '__main__':
    config = get_config_json('config.json')

    xun_fei = XunFeiSDK(config.get('APPId'), config.get('APISecret'), config.get('APIKey'))
    filename = "image/5e5eb526-90e7-4915-8e00-b363f8bce2b2.jpg"
    #读取微信对话截图
    with open(filename, "rb") as f:
        imageBytes = f.read()
    #分割长截图
    image_list = image_split(imageBytes)
    #识别图片
    filename = ''
    for image in image_list:
        image = image_resize(image)
        image_info_str = xun_fei.ocr_request(image)
        if image_info_str is None:
            break
        image_info_json=json.loads(image_info_str)
        lines=image_info_json['pages'][0]['lines']
        dialog=[]
        line_text=''
        y_point=0
        
        for line in lines:
            words, (x, y), color = msg_type(line, image)
            if words is None:
                if line == lines[-1]:
                    dialog.append(line_text)
                continue
            if '自然点的' in words:
                print('')
            # 匹配系统消息
            if words in ['...', '我通过了你的朋友验证请求，现在', '我们可以开始聊天了', '以上是打招呼的内容', '三', '+', '你撤回了一条消息', 'HD', ':', '按住说话']:
                if line == lines[-1]:
                    dialog.append(line_text)
                continue
            # 匹配时间
            if re.findall('.*\d:\d\d.*', words):
                if line == lines[-1]:
                    dialog.append(line_text)
                continue
            # 匹配月份
            if re.findall('(\d{0,1})月\d{0,1}日.*', words):
                if line == lines[-1]:
                    dialog.append(line_text)
                continue
            # 匹配电量
            if dialog == [] and line_text == '':
                try:
                    battery_num = int(words)
                    if battery_num > 0 and battery_num <= 100:
                        continue
                except:
                    pass
            # 匹配备注手机
            search_phone = re.findall(
                '[1][3-9][0-9]{9}', words.replace('-', ''))
            if search_phone:
                phone = search_phone
                filename = words
                continue
            # 匹配文字和角色
            if color[0] > 200:  # 通过背景颜色是白色,判断为好友
                if line_text == '':
                    line_text = '好友:'+words
                elif y-y_point < 40:
                    line_text = line_text+words
                else:
                    dialog.append(line_text)
                    line_text = '好友:'+words
            elif color[0] < 150:  # 通过背景颜色是绿色,判断为自己
                if line_text == '':
                    line_text = '自己:'+words
                elif y-y_point < 40:
                    line_text = line_text+words
                else:
                    dialog.append(line_text)
                    line_text = '自己:'+words
            y_point = y
            if line == lines[-1]:
                dialog.append(line_text)
        #保存识别到的结果文本
        if filename == '':
            with open('result.txt', 'a+', encoding='utf-8') as f:
                for dia in dialog:
                    f.write(dia+'\n')
        else:
            with open(filename.replace('/', '.')+'.txt', 'a+', encoding='utf-8') as f:
                for dia in dialog:
                    f.write(dia+'\n')
