import pyaudio
import numpy as np
import time
import requests
from SpeechModel251 import ModelSpeech
from LanguageModel2 import ModelLanguage
from general_function.file_wav import read_wav_data
import wave

from aip import AipSpeech

API_KEY = 'PotZGWTqDa6bLyAOYVUUersG'
SECRET_KEY = 'sBzLocvhlgGhR9wtkj4jisefYTFkwkLb'
APP_ID = '21930573'
AUDIO_FILE = 'test.wav'
DEV_PID = 1537
client = AipSpeech(appId=APP_ID, apiKey=API_KEY, secretKey=SECRET_KEY)

CHUNK = 1024
CHANNELS = 1
RATE = 16000
FORMAT = pyaudio.paInt16
datapath = './'
modelpath = 'model_speech/'
ms = ModelSpeech(datapath)
ms.LoadModel(modelpath + 'speech_model251_e_0_step_625000.model')

ml = ModelLanguage('model_language')
ml.LoadModel()


def findInternalRecordingDevice(p):
    # 要找查的设备名称中的关键字
    target = '立体声混音'
    # 逐一查找声音设备
    for i in range(p.get_device_count()):
        devInfo = p.get_device_info_by_index(i)
        if devInfo['name'].find(target) >= 0 and devInfo['hostApi'] == 0:
            # print('已找到内录设备,序号是 ',i)
            return i
    print('无法找到内录设备!')
    return -1


def read_buffer_data(buff_data):
    wave_data = np.frombuffer(buff_data, dtype=np.short)  # 将声音文件数据转换为数组矩阵形式
    wave_data.shape = -1, CHANNELS  # 按照声道数将数组整形，单声道时候是一列数组，双声道时候是两列的矩阵
    wave_data = wave_data.T  # 将矩阵转置
    # wave_data = wave_data
    return wave_data


def save_buffer_data2wav(buff_data):
    # 创建pyAudio对象
    p = pyaudio.PyAudio()
    # 打开用于保存数据的文件
    wf = wave.open(AUDIO_FILE, 'wb')
    # 设置音频参数
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(RATE)
    # 写入数据
    wf.writeframes(buff_data)
    # 关闭文件
    wf.close()
    # 结束pyaudio
    p.terminate()


# 实时识别语音
def callback(data, frame_count, time_info, status):
    # wave_data = read_buffer_data(data)
    save_buffer_data2wav(data)
    return data, pyaudio.paContinue


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def record():
    p = pyaudio.PyAudio()
    dev_idx = findInternalRecordingDevice(p)
    if dev_idx < 0:
        return
    # 在打开输入流时指定输入设备
    stream = p.open(input_device_index=dev_idx,
                    format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback
                    )
    stream.start_stream()
    while stream.is_active():
        text = client.asr(get_file_content(AUDIO_FILE), 'wav', RATE, {
            'dev_pid': DEV_PID,
        })
        print(text)
        # print(''.join(text['result']).strip('。'))

        time.sleep(1)
    stream.stop_stream()
    stream.close()
    p.terminate()


def main():
    record()


if __name__ == '__main__':
    main()
