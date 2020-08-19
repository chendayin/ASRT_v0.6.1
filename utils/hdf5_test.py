import h5py


def write():
    f = h5py.File("test.h5", 'w')
    f['data'] = range(100)
    f.close()


def read():
    f = h5py.File('test.h5', 'r')
    print(f.get('data')[:10])


def main():
    write()
    read()


if __name__ == '__main__':
    main()
