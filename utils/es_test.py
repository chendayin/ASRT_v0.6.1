from elasticsearch import Elasticsearch
from datetime import datetime
import certifi


def main():
    es = Elasticsearch(["localhost:9200"])
    body = {"name": 'lucy', 'sex': 'female', 'age': 10}
    es.index(index="index", doc_type="type", body=body)


if __name__ == '__main__':
    main()
