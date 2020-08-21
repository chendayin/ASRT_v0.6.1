from Mysql_pool_utils import MyPoolDB
import glob

DB_POOL = MyPoolDB(host="192.168.1.114", user="wst_cfg", password="5560203@Wst", db_base="taobao_live", max_num=5)


def read_txt(path):
    paths = glob.glob(path)
    for path in paths:
        with open(path, encoding="utf-8") as f:
            for word in f:
                yield word.strip()


def get_db_cursor():
    db = DB_POOL.get_connect()
    cursor = db.cursor()
    return db, cursor


def main():
    g = read_txt(r"D:\工作\ASRT_v0.6.1\sensitive_data\*.txt")
    db, cursor = get_db_cursor()
    sql = "replace into sensitive_content values ('{}')"
    for word in g:
        try:
            flag = cursor.execute(sql.format(word))
            db.commit()
            if flag > 0:
                print(f"success insert into {word} to mysql")
        except Exception as e:
            print(e)
            continue


if __name__ == '__main__':
    main()
