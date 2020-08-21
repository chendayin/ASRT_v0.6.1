import requests


def main():
    url = "http://livecb.alicdn.com/mediaplatform/3374082f-608d-4c6f-9ebe-4589da4e5cdb.m3u8?auth_key=1600397638-0-0-a900ca068c26c81ba77c729e4859f91e&viewer_id=0&trace_id=0b5206b115978991609465404e2083"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-site': 'cross-site',
        # 'path': '/livecb.alicdn.com/mediaplatform/3374082f-608d-4c6f-9ebe-4589da4e5cdb.flv?auth_key=1597899221-0-0-1b0e2810b43e7f5def8732ab07aed453&ali_redirect_ex_hot=100',
        # 'authority': 'ip4228431070.mobgslb.tbcache.com'
    }

    r = requests.get(url, headers=headers)
    print(r.text)


if __name__ == '__main__':
    main()
