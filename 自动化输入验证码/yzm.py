import ddddocr
import re

from flask import Flask
from flask import request
import base64

app = Flask(__name__)

ocr = ddddocr.DdddOcr(show_ad=False)


@app.route('/api', methods=['POST'])
def api(port):
    app.run(host='0.0.0.0', port=int(port))
    try:
        url = request.form.get('url')
        data = url.replace(' ', '+')
        base64_img = re.search('data:image/png;base64,(.*?)$', data)
        captcha_img = base64.b64decode(base64_img.group(1))
        res = ocr.classification(captcha_img)
        return res
    except Exception as e:
        return '请求失败'


if __name__ == '__main__':
    api(9999)

