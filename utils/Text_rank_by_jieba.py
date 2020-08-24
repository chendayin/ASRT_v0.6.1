import jieba.analyse


def main():
    txt = "网红很仙的裙子网纱半身仙女夏季女中长款春秋长裙不规则黑色纱裙"
    top20 = jieba.analyse.textrank(txt)
    print(top20)


if __name__ == '__main__':
    main()
