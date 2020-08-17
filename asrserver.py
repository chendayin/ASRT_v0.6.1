#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
from SpeechModel251 import ModelSpeech
from LanguageModel2 import ModelLanguage
from aip import AipNlp

API_KEY = 'jly4sifius2N8eufoXKigo2H'
SECRET_KEY = 'ZaK0pgQloBBc8k9KBYHx1AEmflMpoPO1'
APP_ID = '22062243'

datapath = './'
modelpath = 'model_speech/'
ms = ModelSpeech(datapath)
ms.LoadModel(modelpath + 'speech_model251_e_0_step_625000.model')

ml = ModelLanguage('model_language')
ml.LoadModel()


def text_corrector(text):
    client = AipNlp(appId=APP_ID, apiKey=API_KEY, secretKey=SECRET_KEY)
    result = client.ecnet(text)
    print(result)
    if "error_code" in result:
        pass
    else:
        return result['item']['correct_query']


class TestHTTPHandle(http.server.BaseHTTPRequestHandler):
    def setup(self):
        self.request.settimeout(10)
        http.server.BaseHTTPRequestHandler.setup(self)

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("get 方法被调用")
        buf = 'ASRT_SpeechRecognition API'
        self.protocal_version = 'HTTP/1.1'

        self._set_response()

        buf = bytes(buf, encoding="utf-8")
        self.wfile.write(buf)

    def do_POST(self):
        '''
        处理通过POST方式传递过来并接收的语音数据
        通过语音模型和语言模型计算得到语音识别结果并返回
        '''
        path = self.path
        print(path)
        # 获取post提交的数据
        datas = self.rfile.read(int(self.headers['content-length']))
        # datas = urllib.unquote(datas).decode("utf-8", 'ignore')
        datas = datas.decode('utf-8')
        datas_split = datas.split('&')
        token = ''
        fs = 0
        wavs = []

        for line in datas_split:
            [key, value] = line.split('=')
            if 'wavs' == key and '' != value:
                wavs.append(int(value))
            elif 'fs' == key:
                fs = int(value)
            elif 'token' == key:
                token = value
            else:
                print(key, value)

        if token != 'qwertasd':
            buf = '403'
            print(buf)
            buf = bytes(buf, encoding="utf-8")
            self.wfile.write(buf)
            return
        if len(wavs) > 0:
            r = self.recognize([wavs], fs)
        else:
            r = ''

        if token == 'qwertasd':
            buf = r
        else:
            buf = '403'

        self._set_response()
        buf = bytes(buf, encoding="utf-8")
        self.wfile.write(buf)

    def recognize(self, wavs, fs):
        r = ''
        try:
            r_speech = ms.RecognizeSpeech(wavs, fs)
            print(r_speech)
            str_pinyin = r_speech
            r = ml.SpeechToText(str_pinyin)
            r = text_corrector(r)
        except:
            r = ''
            print('[*Message] Server raise a bug. ')
        return r


def start_server(ip, port):
    http_server = http.server.HTTPServer((ip, int(port)), TestHTTPHandle)

    print('服务器已开启')

    try:
        http_server.serve_forever()  # 设置一直监听并接收请求
    except KeyboardInterrupt:
        pass
    http_server.server_close()
    print('HTTP server closed')


if __name__ == '__main__':
    start_server('', 20000)  # For IPv4 Network Only
