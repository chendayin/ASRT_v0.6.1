#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
from general_function.file_wav import *
import time

t = time.time()

url = 'http://127.0.0.1:20000/'

token = 'qwertasd'

wavsignal, fs = read_wav_data('20170001P00297A0112.wav')
datas = {'token': token, 'fs': fs, 'wavs': wavsignal}

r = requests.post(url, datas)

r.encoding = 'utf-8'

print(r.text)

print(f'花费时间{time.time() - t}s')
