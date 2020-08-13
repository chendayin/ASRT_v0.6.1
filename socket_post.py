import socket

RATE = 16000


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


if __name__ == '__main__':
    connect_socket('[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]')
