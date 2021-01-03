import requests
import time
import signal

API_HOST = 'https://openapi.naver.com/v1/search/news.json'
API_CLIENT_ID = 'WspdN2NYUPK3Q4Bhurlj'
API_CLIENT_SECRET = 'AFSUp_3FsX'

API_HEADERS = {'X-Naver-Client-Id': API_CLIENT_ID,
            'X-Naver-Client-Secret': API_CLIENT_SECRET}

def processInit(msgQueue):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    time.sleep(4)
    import django
    import os
    #별도 프로세스에서 장고 모델을 사용하기 위해서는 새로운 장고를 초기화해야한다....
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ASTS.settings")
    if os.environ.get("RUN_CRAWL") != "true" and os.environ.get("RUN_MAIN") == "true":
        os.environ["RUN_CRAWL"] = 'true'
        django.setup()
        print("now crawling process has been started and it is wating for kill signal. 섹스")
        while True:
            if not msgQueue.empty():
                if msgQueue.get() == 'exit':
                    break
            work()
            time.sleep(5)
        print("now crawling process is terminated. wating for parent process to be terminated")
        
def work():
    from . import models
    print(models.CrawlingKeyword.objects.all())
    print("crawling work step has been done. wating for another step...")

def main():
    #최신 한 페이지를 받아오는 시험용 코드
    params = {'query': '원유',
            'display': 10,
            'start': 1,
            'sort': 'sim'}#날짜순은 'date'
    res = requests.get(API_HOST, headers=API_HEADERS, params=params)
    print(res.status_code)
    jsonRes = res.json()

    #지금은 유사도순 정렬이지만 날짜순으로 정렬하고 10개씩 가져오면서 더이상 새로운(DB에 기록되지 않음) 것이 없다면 뒷페이지를 가져오는 것을 멈추면 된다.

    #json을 테스트 목적으로 순회한다.
    for obj in jsonRes:
        print(obj)
    for item in jsonRes['items']:
        print('제목 :', item['title'])
        print('요약 설명 :', item['description'])
        print('언론사링크 :', item['originallink'])
        print('네이버링크 :', item['link'])

#이것은 크롤러가 메인으로 따로 실행될 때의 코드이다.
if __name__ == "__main__":
    # execute only if run as a script
    main()