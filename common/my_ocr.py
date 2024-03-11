import re

import easyocr
import numpy


def read_img(capture_img):
    reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
    text = reader.readtext(numpy.asarray(capture_img))
    return text


def read_img_path(img_path):
    reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
    text = reader.readtext(img_path, detail=0, paragraph=True)
    return text


if __name__ == '__main__':
    # 截图征召码
    result = read_img_path('test.png')
    print(result[1])
    match_obj = re.search(r'~[\w\s]*~', result[1])
    match_str = match_obj.group()
    print(re.sub(r'\s', '', match_str))
