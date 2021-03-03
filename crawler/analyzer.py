import json
from datetime import datetime

from elasticsearch import NotFoundError
import os
import elasticsearch


def analysis():
    print("analysis 실행")
    if os.environ.get("ELK_ADDR") is None:  # 도커로 실행 될때에는 url이 수정되어야 하기 때문에 변경
        elk_addr = "http://localhost:9200"
    else:
        elk_addr = os.environ.get("ELK_ADDR")
    es_client = elasticsearch.Elasticsearch(elk_addr)

    from crawler.models import NewsKeyword

    for keyword in set(NewsKeyword.objects.values_list('keyword',flat=True)):
        if keyword == "원유":
            with open('./data-analysis-json/crude-oil.json',encoding='UTF-8') as json_file:
                query_body = json.load(json_file)
        else:
            break

        try:
            results = es_client.search(index='news', body=query_body)
            rank_url = list()
            from . import models
            for result in results['hits']['hits']:
                print('score', result['_score'], 'source:', result['_source'])
                rank_url.append(str(result['_id']))

            # if len(results['hits']['hits']) < 5:  # 값이 5개보다 적으면 빈 값을 돌려줘야함
            #     for ranks in range(5 - len(results['hits']['hits'])):
            #         rank_list.append(None)

            print(rank_url)

            for idx, rank in enumerate(rank_url):
                models.Classification.objects.update_or_create(
                    defaults={'date': datetime.now().strftime('%Y-%m-%d'), 'type': keyword, 'news_url': rank[idx],
                              'rank': (idx + 1)},
                )

        except NotFoundError:
            print("첫 실행이라 인덱스가 없음")




    # results = es_client.search(index="news", body={"query": {"match_all": {}}})    # 모든 값을 가져옴

