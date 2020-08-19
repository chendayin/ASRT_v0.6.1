import pycorrector
import time


def main():
    corrected_sent, detail = pycorrector.correct('神么东西')
    print(corrected_sent, detail)


if __name__ == '__main__':
    start = time.time()
    main()
    print(f"cost time {time.time() - start}")
