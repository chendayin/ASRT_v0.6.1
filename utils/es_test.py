from elasticsearch import Elasticsearch
from datetime import datetime
import certifi


def main():
    es = Elasticsearch(["localhost:9200"])
    print(es.info())


if __name__ == '__main__':
    main()
