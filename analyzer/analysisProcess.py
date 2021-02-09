import os

import elasticsearch


def processInit(msgQueue):

    try:
        if os.environ.get("RUN_ANAL") != "true" and os.environ.get("RUN_MAIN") == "true":
            os.environ["RUN_ANAL"] = 'true'

        if os.environ.get("ELK_ADDR") is None:      # 도커로 실행 될때에는 url이 수정되어야 하기 때문에 변경
            elk_addr = "http://localhost:9200"
        else:
            elk_addr = os.environ.get("ELK_ADDR")

        es_client = elasticsearch.Elasticsearch(elk_addr)

        es_client.ping()

        query_body = {                  # 예제 쿼리, 나중에는 JSON 형태로 따로 파일을 만들어서 관리
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "body_text": "금"
                        }
                    }
                }
            }
        }

        results = es_client.search(index='news', body=query_body)
        #results = es_client.search(index="news", body={"query": {"match_all": {}}})    # 모든 값을 가져옴

        for result in results['hits']['hits']:
            print('score', result['_score'], 'source:', result['_source'])

    except Exception as e:
        print("예외 발생", e)

