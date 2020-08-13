import pyaudio
import numpy as np
import time
import requests
import socket

CHUNK = 1024
CHANNELS = 1
RATE = 16000
FORMAT = pyaudio.paInt16


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


def connect_socket(wave_data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    token = 'qwertasd'
    client.setblocking(False)  # 这里设置成非阻塞
    try:
        client.connect(("127.0.0.1", 20000))  # 阻塞不会消耗cpu
    except BlockingIOError as e:
        pass
    while True:
        try:
            post_request_info = '''POST /index HTTP/1.1
            Host: 127.0.0.1:20000
            Content-Type: application/x-www-form-urlencoded
            Content-Length: 28
            
            token={}&fs={}&wavs={}'''.format(token, RATE, wave_data)
            client.send(post_request_info.encode('utf8'))
            res = client.recv(1024)
            print(res)
            break
        except OSError as e:
            pass


def recognition(wave_data):
    url = 'http://127.0.0.1:20000/'
    token = 'qwertasd'
    data = {'token': token, 'fs': RATE, 'wavs': wave_data}
    r = requests.post(url, data)

    r.encoding = 'utf-8'

    return r.text


# 实时识别语音
def callback(data, frame_count, time_info, status):
    wave_data = read_buffer_data(data)
    print(wave_data)
    connect_socket(wave_data)
    return data, pyaudio.paContinue


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
        time.sleep(10)
    stream.stop_stream()
    stream.close()
    p.terminate()


def main():
    record()


if __name__ == '__main__':
    main()
