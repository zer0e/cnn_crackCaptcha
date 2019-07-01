import requests
import os,random,hashlib,string,base64,json
url = "http://47.106.103.222:8000/captcha"
oldpath = 'images/origin/'

image_list = os.listdir(oldpath)
i = 1
error = []
print(image_list)

def get_code_from_internet(file_name):
    data = {}
    path = ""
    #print(file_name)
    with open(path + file_name, "rb") as f:
        data0 = f.read()
        data['image_base64'] = str(base64.b64encode(data0),'utf-8')
        data['app_id'] = '123456'
        data['ocr_code'] = '0001'
    headers={'Content-Type':'application/json'}
    res = requests.post(url='https://nmd-ai.juxinli.com/ocr_captcha',headers=headers,data=json.dumps(data))
    res = res.json()
    return res['string']
def get_code():
    global image_list
    global i
    global error
    for image in image_list:
        try:
            code = get_code_from_internet(oldpath + image)
            print(code)
            n = ''.join(random.sample(string.ascii_letters+string.digits, 32))
            m = hashlib.md5()
            m.update(n.encode("utf-8"))
            result = m.hexdigest()
            os.rename(os.path.join(oldpath,image), os.path.join(oldpath, (code + "_" + result + ".jpg")))
        except Exception:
            #print("error")
            error.append(image)
        finally:
            print(i)
            i += 1
def main():
    get_code()
    print(error)

if __name__ == "__main__":
    main()





