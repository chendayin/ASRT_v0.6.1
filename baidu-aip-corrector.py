from aip import AipNlp

API_KEY = 'jly4sifius2N8eufoXKigo2H'
SECRET_KEY = 'ZaK0pgQloBBc8k9KBYHx1AEmflMpoPO1'
APP_ID = '22062243'


def text_corrector(text):
    client = AipNlp(appId=APP_ID, apiKey=API_KEY, secretKey=SECRET_KEY)
    result = client.ecnet(text)
    if "error_code" in result:
        pass
    else:
        return result['item']['correct_query']


if __name__ == '__main__':
    r = text_corrector("你什么东西哦")
    print(r)
