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


    try:
        results = es_client.search(index='news', body=query_body)
        rank_list = list()
        from . import models
        for result in results['hits']['hits']:
            print('score', result['_score'], 'source:', result['_source'])
            rank_list.append(str(result['_source']['body_text']))

        if len(results['hits']['hits']) < 5:            # 값이 5개보다 적으면 빈 값을 돌려줘야함
            for ranks in range(5-len(results['hits']['hits'])):
                rank_list.append("")

        models.Recommend.objects.update_or_create(
            defaults={'ranked_date': datetime.now().strftime('%Y-%m-%d'), 'rank1': rank_list[0], 'rank2': rank_list[1],
                      'rank3': rank_list[2], 'rank4': rank_list[3], 'rank5': rank_list[4]},
            ranked_date = datetime.now().strftime('%Y-%m-%d')
        )
    except NotFoundError:
        print("첫 실행이라 인덱스가 없음")


    # results = es_client.search(index="news", body={"query": {"match_all": {}}})    # 모든 값을 가져옴

