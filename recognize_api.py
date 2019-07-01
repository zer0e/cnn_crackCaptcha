from flask import Flask,request
from PIL import Image
import base64,json
from model import Model


app = Flask(__name__)
# skl_model = Model("skl_captcha_model")
# print(skl_model.predict_from_img(Image.open("test.jpg")))

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/captcha',methods=['GET', 'POST'])
def captcha():
    if request.method == 'GET':
        msg = {'msg': 'not image'}
        return json.dumps(msg)
    else:
        global skl_model
        img_base64 = request.form['data']
        img = base64.b64decode(img_base64)
        with open("test.jpg",'wb') as f:
            f.write(img)
            f.close()
        img = Image.open("test.jpg")
        code = skl_model.predict_from_img(img)
        msg = {'code': code }
        return json.dumps(msg)

if __name__ == '__main__':
    skl_model = Model("skl_captcha_model")
    app.run(threaded=False)
# from flask import Flask,request
# from flask_restful import Resource, Api
# import base64
# from model import Model

# app = Flask(__name__)
# api = Api(app)

# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}

# class Captcha(Resource):

#     def get(self):
#         return {"msg": 'not image'}
#     def post(self):
#         img_base64 = request.form('data')
#         img = base64.b64decode(img_base64)
#         code = skl_model.predict_from_img(img)
#         return {"code": code}

# api.add_resource(HelloWorld, '/')
# api.add_resource(Captcha, '/captcha')


# if __name__ == '__main__':
#     skl_model = Model("skl_captcha_model")
#     app.run(debug=True)