import requests
import base64
import time

url = 'http://127.0.0.1:5000/captcha'

time1 = time.time()
for i in range(1000):

    with open("images/examples/5295_2997b4e0879c82e85eda6ba3b7dc58d7.jpg", "rb") as f:
        data0 = f.read()
        data = {
            'data': str(base64.b64encode(data0),'utf-8')
        }
        # print(data)
        res = requests.post(url=url,data=data)
        # print(res.text)
        res = res.json()
        # print(res['code'])
print(time.time() - time1)