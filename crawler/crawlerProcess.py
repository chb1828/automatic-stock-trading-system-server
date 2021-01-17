import requests
import time
import signal
import maya
import re
import os
from bs4 import BeautifulSoup

#네이버 api의 1일 검색 허용량은 25000회이며, 초당 10회 미만의 요청을 보내야 합니다.

API_HOST = 'https://openapi.naver.com/v1/search/news.json'
API_CLIENT_ID = 'WspdN2NYUPK3Q4Bhurlj'
API_CLIENT_SECRET = 'AFSUp_3FsX'

API_HEADERS = {'X-Naver-Client-Id': API_CLIENT_ID,
            'X-Naver-Client-Secret': API_CLIENT_SECRET}

NEWS_CRAWLER_HEADERS = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"
}

#날짜 제한, 기본적으로 30일 이내의 뉴스기사만을 가져온다.
CRAWLER_BACKTRACK_LIMIT = 30

#if you want some default keywords, add them in here for easy test
keywords = ["원유", "금", "은", "미국채"]

cleaner = re.compile('(<.*?>|&.*;)')
#descriptionRegex = re.compile(r"(?:[.]\s)([^.]+)(?:[.]{1, 3})$")
descriptionRegex = re.compile(r"([^.]+)(?:[.]*[ ]*$)")

globalQueue = None

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

        from . import models

        keywordModels = [ models.CrawlingKeyword.objects.get_or_create(keyword = keywords[x]) for x in range(len(keywords))]
        print(keywordModels)
        for keywordModel in keywordModels:
            if keywordModel[1] == True:
                keywordModel[0].save()
                print("saving", keywordModel[0])
            else:
                print("already have", keywordModel[0])

        global globalQueue
        globalQueue = msgQueue
        while True:
            if checkKillSignal():
                break
            work()
            #break
            time.sleep(1)
        print("now crawling process is terminated. wating for parent process to be terminated")
        
def work():
    from . import models
    keywords = models.CrawlingKeyword.objects.all()

    #naver 검색 api는 같은 것을 여러 번 돌려주기도 한다. 이것은 스스로 걸러내야 한다.
    urlCheckSet = set()

    #text tag and escape cleaner

    if len(keywords) != 0:
        for keywordModel in keywords:
            if checkKillSignal():
                break
            print('searching news for keyword', keywordModel.keyword)
            #뉴스의 모든 페이지를 다 검색할 때까지 보거나, 뉴스의 한 페이지에서 더이상 새것이 하나도 없을 때 까지 검색한다.
            #단, 날짜는 한 달 전 것 까지만 검색한다. 모든 뉴스를 다 긁을 수도 있지만, 네이버에서 원유 관련해서 나오는 뉴스만 62만개이다.
            start = 1
            stop = False
            #우선 모든 뉴스페이지를 검색한다.
            while not stop and not checkKillSignal():
                params = {'query': keywordModel.keyword,
                        'display': 100,#100 is max
                        'start': start,
                        'sort': 'date'}#날짜순은 'date', 유사도는 sim
                res = requests.get(API_HOST, headers=API_HEADERS, params=params)
                print('status code', res.status_code)
                jsonRes = res.json()
                
                for item in jsonRes['items']:
                    title = re.sub(cleaner, '', item['title'])
                    print('제목 :', title)
                    print('날짜 :', item['pubDate'])
                    print('링크', item['originallink'])
                    backTrackDate = maya.now().add(days = -30)
                    print(backTrackDate, type(backTrackDate))
                    pubDate = maya.parse(item['pubDate'])
                    print(pubDate, type(pubDate))
                    
                    if urlCheckSet.issuperset({item['originallink']}):
                        print(item['originallink'], "는 중복된 링크입니다.")
                    else:
                        urlCheckSet.add(item['originallink'])
                        #해당 신문사의 기사를 직접 읽어들인다.
                        page = requests.get(item['originallink'], headers = NEWS_CRAWLER_HEADERS)
                        soup = BeautifulSoup(re.sub(cleaner, '', page.text).replace("  ", " "), 'html.parser')
                        #print(soup)
                        #print(soup)
                        #수프의 강력한 기능으로, 우리는 기사 요약이 있던 텍스트가 포함된 요소를 찾아내고 그 요소의 텍스트만을 추출한다.
                        #파이썬은 잘 작동하는 아름다운 연장과 같다. 섹스......
                        description = re.sub(cleaner, '', item['description'])
                        #검색결과 요약의 강조문을 지운다.

                        #[^.]+$는 마지막 마침표 이후의 문장을 가져온다고 한다.
                        print("요약 :", description, "end")
                        result = descriptionRegex.search(description)
                        print(result)
                        if result:
                            bsSearchTarget = result.group(result.lastindex)
                            print("정규식 결과", bsSearchTarget)
                            targetElements = soup.find_all(recursive = True , text = re.compile("[.]*"+bsSearchTarget+"[.]*"))
                            print("탐색결과", targetElements)
                            if len(targetElements) == 0:
                                print("탐색 실패함")
                                if not os.path.exists("./newsbackup"):
                                    os.mkdir("./newsbackup")
                                if res.encoding == "UTF-8":
                                    f = open("./newsbackup/"+title+'.txt', 'w', -1, 'utf-8')
                                else:
                                    f = open("./newsbackup/"+title+'.txt', 'w', -1)
                                f.write(page.text)
                                f.close()
                            else:
                                print("탐색 성공함")
                            time.sleep(1)
                        else:
                            print("정규식 일치 없음")
                        if not checkKillSignal():
                            #신문사의 기사를 읽어들이는 과정에서 크롤러가 신문사 웹사이트 요청 제한을 초과해버리면 아무 것도 받아오지 못하게 된다.
                            time.sleep(1)
                        else:
                            stop = True
                            break


                    if pubDate.epoch < backTrackDate.epoch :
                        print("날짜 제한이 지났습니다. 해당 키워드 크롤링을 중단합니다.")
                        stop = True
                        break

                    #print('요약 설명 :', item['description'])
                    #print('언론사링크 :', item['originallink'])
                    #print('네이버링크 :', item['link'])
                
                
                #json을 테스트 목적으로 순회한다.
                print('------------------')
                print('전체', jsonRes['total'])
                print('시작', jsonRes['start'])
                print('표시갯수', jsonRes['display'])
                print('------------------')

                #901 means it crawled all the allowed 1000 from naver news api. it doeesnt even return result after 1000th news.
                if (start + jsonRes['display'] - 1 == jsonRes['total']) or start == 901:
                    stop = True
                else:
                    start = start + jsonRes['display']

                #minimum sleep for request per second limitation.
                time.sleep(0.2)

    else:
        print('There is no keyword for search, config CrawlingKeyword table if you want to let it work')

    print("crawling work step has been done. wating for another step...")

def checkKillSignal():
    global globalQueue
    if not globalQueue.empty():
        if globalQueue.get() == 'exit':
            globalQueue.put('exit')#put that msg back for the call chain.
            return True
    return False


def main():
    #최신 한 페이지를 받아오는 시험용 코드
    params = {'query': '원유',
            'display': 10,
            'start': 1,
            'sort': 'sim'}#날짜순은 'date'
    res = requests.get(API_HOST, headers=API_HEADERS, params=params)
    print('status code', res.status_code)
    jsonRes = res.json()

    #지금은 유사도순 정렬이지만 날짜순으로 정렬하고 10개씩 가져오면서 더이상 새로운(DB에 기록되지 않음) 것이 없다면 뒷페이지를 가져오는 것을 멈추면 된다.

    #json을 테스트 목적으로 순회한다.
    print('display', jsonRes['display'])
    print('total', jsonRes['total'])
    print('start', jsonRes['start'])

    for item in jsonRes['items']:
        print('제목 :', item['title'])
        print('요약 설명 :', item['description'])
        print('언론사링크 :', item['originallink'])
        print('네이버링크 :', item['link'])
        print('발행일 : ', item['pubDate'])

#이것은 크롤러가 메인으로 따로 실행될 때의 코드이다.
if __name__ == "__main__":
    # execute only if run as a script
    main()