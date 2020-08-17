import time
import wave

import requests
import numpy as np
import pyaudio
import threading
import websocket
from aip import AipSpeech

API_KEY = 'PotZGWTqDa6bLyAOYVUUersG'
SECRET_KEY = 'sBzLocvhlgGhR9wtkj4jisefYTFkwkLb'
APP_ID = '21930573'


AUDIO_FILE = 'out.wav'
DEV_PID = 1537
CHUNK = 1024
CHANNELS = 1
RATE = 16000

client = AipSpeech(appId=APP_ID, apiKey=API_KEY, secretKey=SECRET_KEY)


# 录音类 监听声卡
class Record:
    def __init__(self):
        self.CHUNK = CHUNK
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = CHANNELS
        self.RATE = RATE
        self._running = True
        self._frames = []

    # 获取内录设备序号,在windows操作系统上测试通过，hostAPI = 0 表明是MME设备
    def findInternalRecordingDevice(self, p):
        # 要找查的设备名称中的关键字
        target = '立体声混音'
        # 逐一查找声音设备
        for i in range(p.get_device_count()):
            devInfo = p.get_device_info_by_index(i)
            print(devInfo)
            if devInfo['name'].find(target) >= 0 and devInfo['hostApi'] == 0:
                # print('已找到内录设备,序号是 ',i)
                return i
        print('无法找到内录设备!')
        return -1

    # 开始录音，开启一个新线程进行录音操作
    def start(self):
        threading._start_new_thread(self.__record, ())

    # 执行录音的线程函数
    def __record(self):
        self._running = True
        self._frames = []

        p = pyaudio.PyAudio()
        # 查找内录设备
        dev_idx = self.findInternalRecordingDevice(p)
        if dev_idx < 0:
            return
        # 在打开输入流时指定输入设备
        stream = p.open(input_device_index=dev_idx,
                        format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        # 循环读取输入流
        while self._running:
            data = stream.read(self.CHUNK)
            self._frames.append(data)
        # 停止读取输入流
        stream.stop_stream()
        # 关闭输入流
        stream.close()
        # 结束pyaudio
        p.terminate()
        return


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def recognition():
    text = client.asr(get_file_content(AUDIO_FILE), 'wav', RATE, {
        'dev_pid': DEV_PID,
    })
    return ''.join(text['result']).strip('。')


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


def main():
    record = Record()
    record.start()
    running = True
    while running:
        time.sleep(2)
        save_buffer_data2wav(b''.join(record._frames))
        record._frames = []
        try:
            txt = recognition()
        except:
            continue
        print(txt, end='')


if __name__ == '__main__':
    main()
