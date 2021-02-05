import os

import elasticsearch


def processInit():

    try:
        if os.environ.get("RUN_ANAL") != "true" and os.environ.get("RUN_MAIN") == "true":
            os.environ["RUN_ANAL"] = 'true'

        es_client = elasticsearch.Elasticsearch("http://localhost:9200")        #도커로 실행 될때에는 url이 수정되어야함...

        es_client.ping()
        query_body = {
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
        #results = es_client.search(index="news", body={"query": {"match_all": {}}})       

        print(results)

        for result in results['hits']['hits']:
            print('score', result['_score'], 'source:', result['_source'])

    except Exception as e:
        print("예외 발생",e)

