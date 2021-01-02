from django.apps import AppConfig

from multiprocessing import Process, Queue
import signal
from . import crawlerProcess
import time
import os
import atexit

msgQueue = Queue()
p = None

class CrawlerConfig(AppConfig):
    name = 'crawler'
    verbose_name = 'Crawling Service App for ASTS'
    
    def ready(self):
        print('Crawler Service App has been loaded. now starting Crawler Process...')
        global msgQueue
        global p
        #장고의 manage.py는 오토리로드기능을 위해서 두 개의 서버를 실행한다고 한다.
        if os.environ.get("RUN_MAIN") == "true":
            p = Process(target=crawlerProcess.processInit, args=(msgQueue,))
            p.start()
            atexit.register(self.sigStopHandler)

    def sigStopHandler(self):
        print("Ctrl+C has been pressed, now sending kill msg to queue...")
        global msgQueue
        msgQueue.put("exit")
        global p
        p.join()
        print("Crawler process has been terminated. Shutting down...")