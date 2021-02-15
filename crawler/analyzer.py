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
    query_body = {  # 예제 쿼리, 나중에는 JSON 형태로 따로 파일을 만들어서 관리
        "size": 5,
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "body_text": "원유"           # 여기에는 항상 존재하는 값만 찾아온다
                        },
                    },
                    # {
                    #     "range": {
                    #         "crawled_date": {             # 여기에는 뉴스가 게시된 날짜 필드가 들어가야한다.
                    #             "gte": "now-1d/d",
                    #             "lte": "now/d"
                    #         }
                    #     }
                    # }
                ],
                "should": [
                    {
                        "match": {
                            "body_text": "기대감"        # 여기에는 값이 있으면 score 가 올라간다.
                        },
                        "match": {
                            "body_text": "상승"
                        },
                        "match": {
                            "body_text": "증가"
                        },
                    },
                    {
                        "match_phrase": {  # 단어가 아닌 문장 검색
                            "body_text": "연속 증가세"
                        }
                    }
                ],
                "minimum_should_match": 0           # 최소 적용 조건이 0이기 때문에 매치하지 않아도 가져온다.
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

