import socket
from general_function.file_wav import read_wav_data


def connect_socket(wave_data, rate):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    token = 'qwertasd'
    client.setblocking(False)  # 这里设置成非阻塞
    try:
        client.connect(("127.0.0.1", 20000))  # 阻塞不会消耗cpu
    except BlockingIOError as e:
        pass
    while True:
        try:
            post_request_info = 'POST /index HTTP/1.1\r\nHost: 127.0.0.1:20000\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 300\r\n\r\ntoken={}&fs={}&wavs={}'.format(
                token, RATE, wave_data).encode('utf-8')

            # get_request_info = b"""GET /index HTTP/1.1\r\nHost: 127.0.0.1:20000\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nAccept-Encoding: gzip, deflate\r\n\r\n"""

            client.send(post_request_info)
            res = client.recv(1024)
            print(res)
            break
        except OSError as e:
            pass


if __name__ == '__main__':
    wave_data, RATE = read_wav_data('20170001P00001A0006.wav')
    connect_socket(wave_data, RATE)
