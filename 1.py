import wave
import pyaudio


# 保存录音文件
def saveWav():
    CHUNK = 1024
    format = pyaudio.paInt16
    CHANNELS = 1  # 声道数
    RECORD_SECONDS = 10  # 录音的时长
    WAVE_OUTPUT_FILENAME = "out.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    channels=CHANNELS,
                    rate=16000,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("*" * 10, "开始录音：请在4秒内输入语音")
    frames = []
    for i in range(0, int(16000 / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("*" * 10, "录音结束\n")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()


if __name__ == '__main__':
    saveWav()
