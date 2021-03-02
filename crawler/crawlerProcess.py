import requests
import time
import signal
import maya
import re
import os
import datetime
from bs4 import BeautifulSoup, Comment, Tag
from django.utils.text import get_valid_filename
from collections import deque
from selenium import webdriver

#네이버 api의 1일 검색 허용량은 25000회이며, 초당 10회 미만의 요청을 보내야 합니다.
from crawler import analyzer

API_HOST = 'https://openapi.naver.com/v1/search/news.json'
API_CLIENT_ID = 'WspdN2NYUPK3Q4Bhurlj'
API_CLIENT_SECRET = 'AFSUp_3FsX'

API_HEADERS = {'X-Naver-Client-Id': API_CLIENT_ID,
            'X-Naver-Client-Secret': API_CLIENT_SECRET}

NEWS_CRAWLER_HEADERS = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

#날짜 제한, 기본적으로 30일 이내의 뉴스기사만을 가져온다.
CRAWLER_BACKTRACK_LIMIT = 30

#if you want some default keywords, add them in here for easy test
keywords = ["원유", "금", "은", "미국채"]

cleaner = re.compile('(<.*?>|&.*;)')
#descriptionRegex = re.compile(r"(?:[.]\s)([^.]+)(?:[.]{1, 3})$")
descriptionRegex = re.compile(r"([^.]+)(?:[.]*[ ]*$)")

multipleSpace = re.compile('  *')

multipleNewLine = re.compile('\\r?\\n\\s*')

displayNone = re.compile('display\\s*:\\s*none', re.IGNORECASE)

globalQueue = None

webDriver = None

def processInit(msgQueue):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    time.sleep(4)
    import django
    import os

    try:

        #별도 프로세스에서 장고 모델을 사용하기 위해서는 새로운 장고를 초기화해야한다....
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ASTS.settings")
        if os.environ.get("RUN_CRAWL") != "true" and os.environ.get("RUN_MAIN") == "true":
            os.environ["RUN_CRAWL"] = 'true'
            django.setup()
            print("now crawling process has been started and it is wating for kill signal. ↖POsexWER↗")
            global webDriver
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            options.add_argument("disable-notifications")
            webDriver = webdriver.Chrome('./webdriver/chromedriver.exe', chrome_options=options)

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
    
    finally:
        webDriver.quit()
        
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
                        addKeywordForNews(item['originallink'], keywordModel.keyword)
                    else:
                        urlCheckSet.add(item['originallink'])

                        #기존 데이터베이스에도 없어야한다.
                        if len(models.News.objects.filter(url=item['originallink'])) >= 1:
                            print(item['originallink'], "는 이미 DB에 있는 링크입니다.")
                            addKeywordForNews(item['originallink'], keywordModel.keyword)
                            continue

                        #해당 신문사의 기사를 직접 읽어들인다.
                        try:
                            handleNews(item['originallink'], title, keywordModel.keyword, str(pubDate))
                        except Exception as e:
                            printError(item['originallink'] , e)
                        analyzer.analysis()

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

def getRealNewsTag(node, targetLength):
    newsText = node.get_text()
    if len(newsText) <= targetLength / 4:
        return None
    for element in node.find_all(True):
        temp = getRealNewsTag(element, targetLength)
        if temp is not None:
            return temp
    newsText = re.sub(multipleNewLine, '\n', newsText)
    newsText = re.sub(multipleSpace, ' ', newsText)
    if len(newsText) > targetLength / 4:
        return node
    else:
        return None

def sweepShortTextTag(node):
    for element in node.find_all(recursive=False):
        recursiveSweepShortTextTag(element)

def recursiveSweepShortTextTag(node):
    text = node.get_text()
    try:
        style = node["style"]
    except:
        style = ""
    if len(text) > 10 and (displayNone.search(style) == None):
        text = node.get_text()
        if len(text) <= 10:
            node.decompose()
            return
        for element in node.find_all(recursive=False):
            recursiveSweepShortTextTag(element)
    else:
        node.decompose()

def printError(url , e):
    if not os.path.exists("./crawler_log"):
        os.mkdir("./crawler_log")
    f = open("./crawler_log/"+ 'error.txt', 'a+', -1, 'utf-8')
    f.write(url)
    f.write("\n#######################################\n")
    f.write(str(e))
    f.write("\n#######################################\n")
    f.close()

def addKeywordForNews(link, keyword):
    from . import models
    models.NewsKeyword.objects.update_or_create(
        defaults = {'url' : link, 'keyword' : keyword},
        url = link,
        keyword = keyword
    )

#main에 작성하는 테스트 코드가 제대로 되면 옮겨오자.
def handleNews(link, title, keyword, pubDate):
    from . import models
    print('handling ' + link)
    try:
        webDriver.get(link)
        print('render finished')
        try:
            webDriver.switch_to.alert.accept()
            webDriver.switch_to.alert.dismiss()
        except:
            print("no more alerts")
    except:
        print("error while loading in chrome")
        return
        #page = requests.get(link, headers = NEWS_CRAWLER_HEADERS, verify=False)
    soup = BeautifulSoup(str(webDriver.find_element_by_tag_name('body').get_attribute("innerHTML")), 'html.parser')
    removeTargets = ['script', 'a', 'img', 'style', 'iframe', 'form', 'fieldset', 'noscript', 'input', 'button']
    targets = soup.find_all(removeTargets, recursive=True)
    for target in targets:
        #print("제거됌", target)
        target.decompose()
    print("decomposing process done")
    for element in soup(text=lambda text: isinstance(text, Comment)):
        element.extract()
    print("comment node removing process done")
    sweepShortTextTag(soup)#짧은 글자 (댓글 달기) 같은 것 날리기
    print("short text sweeping process done")
    #soup.head.clear()
    #for removeTarget in removeList:
        #removeTarget.decompose()
    newsText = soup.get_text()
    newsText = re.sub(multipleNewLine, '\n', newsText)
    newsText = re.sub(multipleSpace, ' ', newsText)

    #낮은 단위에서부터 뉴스 기사 전체 텍스트 분량의 50%를 넘기는 최초의 것을 찾아낸다.
    #아주 짧은 단신의 경우 전혀 가려낼 수가 없다는 단점이 있다. 이런 경우에는...생각해보자.

    realNewsTag = getRealNewsTag(soup, len(newsText))
    if realNewsTag is None:
        return
    realNewsText = realNewsTag.get_text()
    realNewsText = re.sub(multipleNewLine, '\n', realNewsText)
    realNewsText = re.sub(multipleSpace, ' ', realNewsText)
    realNewsText = realNewsText.strip()

    if not os.path.exists("./newsbackup"):
        os.mkdir("./newsbackup")
    f = open("./newsbackup/"+ get_valid_filename(title) +'.txt', 'w', -1, 'utf-8')
    f.write(link)
    f.write("\n#######################################\n")
    f.write(newsText)
    f.write("\n#######################################\n")
    f.write(realNewsText)
    f.write("\n#######################################\n")
    f.write(str(soup.prettify()))
    f.close()

    models.News.objects.update_or_create(
        defaults = {'url' : link, 'head_text' : title, 'body_text' : realNewsText, 'crawled_date' : str(datetime.datetime.now()), 'posted_date' : pubDate},
        url = link
    )
    addKeywordForNews(link, keyword)
    

def main():
    print(len("시발"))#unicode string len test
    try:
        driver = webdriver.PhantomJS()
        driver.set_window_size(1920, 1080)
        driver.get("http://news.mt.co.kr/mtview.php?no=2021013007521118332")
        #print(driver.find_element_by_tag_name('body').get_attribute("innerHTML"))
        f = open("./newsbackup/"+ 'test' +'.txt', 'w', -1, 'utf-8')
        f.write(driver.find_element_by_tag_name('body').get_attribute("innerHTML"))
        f.close()
    except requests.exceptions.SSLError as e:
        print("SSL error, shitty SSL setting of server is suspicious.")
        page = requests.get('https://kizmom.hankyung.com/news/view.html?aid=202101296319o', headers = NEWS_CRAWLER_HEADERS, verify=False)
        print(page.text)
    finally:
        #dont forget to deallocate native resources.
        driver.quit()

#이것은 크롤러가 메인으로 따로 실행될 때의 코드이다.
if __name__ == "__main__":
    # execute only if run as a script
    main()