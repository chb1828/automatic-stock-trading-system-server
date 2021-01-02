from django.apps import AppConfig

from multiprocessing import Process, Queue
import signal
from . import crawlerProcess
import time

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