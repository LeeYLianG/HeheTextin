import requests
import json
import os
from django.conf import settings

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

class CommonOcr(object):
    def __init__(self, img_path):

        self._app_id = 'cbe2f274063ee5a9e6b8ca7d934fad0e'

        self._secret_code = '7bef25d5f70552894ec57c86a3c8f2ed'
        self._img_path = img_path

    def recognize(self):
        # 商铺小票识别
        url = 'https://api.textin.com/robot/v1.0/api/receipt'
        head = {}
        try:
            image = get_file_content(self._img_path)
            head['x-ti-app-id'] = self._app_id
            head['x-ti-secret-code'] = self._secret_code
            result = requests.post(url, data=image, headers=head)
            return result.text
        except Exception as e:
            return e



#
# if __name__ == "__main__":
#     response = CommonOcr(r'C:\Users\Sakura LeeYL\Desktop\图片\微信图片_20221018104408.jpg')
#     print(response.recognize())
#     response = CommonOcr(r'C:\Users\Sakura LeeYL\Desktop\图片\media\download.jpg')
#     print(response.recognize())
#     response = CommonOcr(r'E:\pycharm新建项目\textin\textin\media\download.jpg')
#     print(response.recognize())
#     media_path=os.path.join(settings.MEDIA_ROOT,'download.jpg')
#     print(media_path)
