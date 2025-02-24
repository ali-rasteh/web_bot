# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# import base64
# from PIL import Image
# import io
# import easyocr


# captcha_image = Image.open('./test.png')
# # captcha_text = pytesseract.image_to_string(captcha_image, config='--psm 6').strip()
# # captcha_text = pytesseract.image_to_string(captcha_image)
# captcha_text = pytesseract.image_to_string(captcha_image, lang='eng', config='--psm 7')
# print(f"Extracted CAPTCHA text: {captcha_text}")



# reader = easyocr.Reader(['en'])
# # Read from an image
# results = reader.readtext('./captcha.png')
# for result in results:
#     print(result[1])










# import sys
# import os
# from base64 import b64encode

# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# from twocaptcha import TwoCaptcha

# # in this example we store the API key inside environment variables that can be set like:
# # export APIKEY_2CAPTCHA=1abc234de56fab7c89012d34e56fa7b8 on Linux or macOS
# # set APIKEY_2CAPTCHA=1abc234de56fab7c89012d34e56fa7b8 on Windows
# # you can just set the API key directly to it's value like:
# # api_key="1abc234de56fab7c89012d34e56fa7b8"

# # api_key = os.getenv('APIKEY_2CAPTCHA', 'YOUR_API_KEY')
# api_key = '1b7946ed50efb24f2978806822aea0d5'

# solver = TwoCaptcha(api_key)
# solver = TwoCaptcha(api_key, defaultTimeout=30, pollingInterval=5)


# with open('./images/normal.jpg', 'rb') as f:
#     b64 = b64encode(f.read()).decode('utf-8')
# try:
#     result = solver.normal(b64)


# try:
#     result = solver.normal('./captcha.png')
    # result = solver.normal(
    #         './captcha.png',
    #         numeric=4,
    #         minLen=4,
    #         maxLen=20,
    #         phrase=0,
    #         caseSensitive=0,
    #         calc=0,
    #         lang='en',
    #         # hintImg='./images/normal_hint.jpg',
    #         # hintText='Type red symbols only',
    #     )


# except Exception as e:
#     sys.exit(e)

# else:
#     sys.exit('result: ' + str(result))









# pip install --upgrade capsolver
# export CAPSOLVER_API_KEY='...'
 
import capsolver
import sys
import os
import base64

capsolver.api_key = "CAP-A7BAF779B2EC08D9513D7F5D279FEF58F9FE055EBF6D80E5691C2FA330500777"
 
# img_path = os.path.join(os.Path(__file__).resolve().parent, "queue-it.jpg")
img_path = './captcha.png'
with open(img_path, 'rb') as f:
    solution = capsolver.solve({
        "type": "ImageToTextTask",
        # "websiteURL": "https://www.example.com",
        # "module": "common",
        "module": "module_005",
        # "body": "/9j/4AAQSkZJRgABA......"
        "body": base64.b64encode(f.read()).decode('utf-8')
    })
    print(solution)


    