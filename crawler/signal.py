from django.db.models.signals import post_save
from django.dispatch import receiver
from elasticsearch import NotFoundError

from crawler.models import News
import os
import elasticsearch
import time


@receiver(post_save, sender=News)
def analysis(sender, **kwargs ):
    time.sleep(5)       # postgresql 에서 elasticsearch로 들어가는 시간중 5초 정도의 시간이 필요
    print("analysis 실행")
    if os.environ.get("ELK_ADDR") is None:  # 도커로 실행 될때에는 url이 수정되어야 하기 때문에 변경
        elk_addr = "http://localhost:9200"
    else:
        elk_addr = os.environ.get("ELK_ADDR")
    es_client = elasticsearch.Elasticsearch(elk_addr)
    query_body = {  # 예제 쿼리, 나중에는 JSON 형태로 따로 파일을 만들어서 관리
        "size": 3,
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "body_text": "원유"
                    }
                }
            }
        }
    }
    try:
        results = es_client.search(index='news', body=query_body)
        for result in results['hits']['hits']:
            print('score', result['_score'], 'source:', result['_source'])
    except NotFoundError:
        print("첫 실행이라 인덱스가 없음")


    # results = es_client.search(index="news", body={"query": {"match_all": {}}})    # 모든 값을 가져옴

