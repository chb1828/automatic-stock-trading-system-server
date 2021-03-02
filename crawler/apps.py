from django.apps import AppConfig

from multiprocessing import Process, Queue
from . import crawlerProcess
import os
import atexit

msgQueue = Queue()
p = None


class CrawlerConfig(AppConfig):
    name = 'crawler'
    verbose_name = 'Crawling Service App for ASTS'
    
    def ready(self):
        #장고의 manage.py는 오토리로드기능을 위해서 두 개의 프로세스를 실행한다고 한다.
        #더 큰 문제는 크로울링 프로세스가 장고를 초기화할 때 레디함수가 한 번 더 호출된다는 것이다. 이 모든 것을 다 틀어막아야한다. 쉽지 않다.
        if os.environ.get("RUN_MAIN") == "true" and os.environ.get("RUN_CRAWL") != "true":
            from django import db
            db.connections.close_all()#이것은 리눅스 환경에서 기본값인 fork로 시작되는 프로세스들이 db 컨넥션 공유 에러를 피하도록 한다.
            print('Crawler service app has been loaded. now starting crawler Process...')
            global msgQueue
            global p
            p = Process(target=crawlerProcess.processInit, args=(msgQueue,))
            p.start()
            atexit.register(self.sigStopHandler)

    def sigStopHandler(self):
        print("Stop signal detected, now sending kill msg to queue...")
        global msgQueue
        msgQueue.put("exit")
        global p
        p.join()
        print("Crawler process has been terminated. Shutting down...")