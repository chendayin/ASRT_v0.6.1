import time

import requests
import numpy as np
import pyaudio
import threading
import websocket

CHUNK = 1024
CHANNELS = 1
RATE = 16000


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

    def __recognition(self, wave_data):
        url = 'http://127.0.0.1:20000/'
        token = 'qwertasd'
        data = {'token': token, 'fs': RATE, 'wavs': wave_data}
        r = requests.post(url, data)

        r.encoding = 'utf-8'

        return r.text

    # 识别接口 实时识别声卡录制的声音


def recognition(wave_data):
    url = 'http://127.0.0.1:20000/'
    token = 'qwertasd'
    data = {'token': token, 'fs': RATE, 'wavs': wave_data}
    r = requests.post(url, data)

    r.encoding = 'utf-8'

    return r.text


def read_buffer_data(buff_data):
    wave_data = np.frombuffer(buff_data, dtype=np.short)  # 将声音文件数据转换为数组矩阵形式
    wave_data.shape = -1, CHANNELS  # 按照声道数将数组整形，单声道时候是一列数组，双声道时候是两列的矩阵
    wave_data = wave_data.T  # 将矩阵转置
    # wave_data = wave_data
    return wave_data


def main():
    record = Record()
    record.start()
    running = True
    while running:
        time.sleep(2)
        wave_data = read_buffer_data(b''.join(record._frames))
        print(wave_data)
        record._frames = []
        txt = recognition(wave_data)
        print(txt, end='')


if __name__ == '__main__':
    main()
