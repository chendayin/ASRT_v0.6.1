import time
import glob
from pypinyin import lazy_pinyin, Style
import re

compile = re.compile(r"[\d，。！？a-zA-Z%]")


def readWaveList():
    txts = glob.glob("../train/*.txt")
    print(f"共有{len(txts)}条语音")
    wave_texts = []
    for txt in txts:
        with open(txt, encoding="utf8") as f:
            wave_text = f.read()
            wave_text = compile.sub("", wave_text)

            wave_texts.append(
                txt.split("\\")[1].split(".")[0] + ' ' + ' '.join(lazy_pinyin(wave_text, style=Style.TONE3)) + '\n')
    with open("../dataset/yumeizi/train.syllable.txt", "w", encoding="utf8") as f:
        f.writelines(wave_texts)


def readWaveList2():
    txts = glob.glob("../train/*.txt")
    for txt in txts:
        print(txt)


def main():
    # readWaveList()
    readWaveList2()


if __name__ == '__main__':
    main()
