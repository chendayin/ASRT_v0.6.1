#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import platform as plat

from SpeechModel251 import ModelSpeech
from LanguageModel2 import ModelLanguage
from keras import backend as K

datapath = ''
modelpath = 'model_speech'

system_type = plat.system()  # 由于不同的系统的文件路径表示不一样，需要进行判断
if system_type == 'Windows':
    datapath = '.'
    modelpath = modelpath + '\\'
elif system_type == 'Linux':
    datapath = '.'
    modelpath = modelpath + '/'
else:
    print('*[Message] Unknown System\n')
    datapath = 'dataset'
    modelpath = modelpath + '/'

ms = ModelSpeech(datapath)

ms.LoadModel(modelpath + 'speech_model251_e_0_step_625000.model')

r = ms.RecognizeSpeech_FromFile('D:\\语音数据集\\ST-CMDS-20170001_1-OS\\20170001P00241I0052.wav')

K.clear_session()

print('*[提示] 语音识别结果：\n', r)

ml = ModelLanguage('model_language')
ml.LoadModel()

str_pinyin = r
r = ml.SpeechToText(str_pinyin)
print('语音转文字结果：\n', r)
