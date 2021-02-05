import os
from multiprocessing import Process, Queue
from django.apps import AppConfig
from . import analysisProcess
import atexit

msgQueue = Queue()
p = None

class ApiConfig(AppConfig):
    name = 'api'
    verbose_name = 'Analysis Service App for ASTS'

    def ready(self):
        if os.environ.get("RUN_MAIN") == "true" and os.environ.get("RUN_ANAL") != "true":
            from django import db
            db.connections.close_all()  # 이것은 리눅스 환경에서 기본값인 fork로 시작되는 프로세스들이 db 컨넥션 공유 에러를 피하도록 한다.
            print('Crawler service app has been loaded. now starting crawler Process...')
            global msgQueue
            global p
            p = Process(target=analysisProcess.processInit, args=(msgQueue,))
            p.start()
            atexit.register(self.sigStopHandler)

    def sigStopHandler(self):
        print("Stop signal detected, now sending kill msg to queue...")
        global msgQueue
        msgQueue.put("exit")
        global p
        p.join()
        print("Crawler process has been terminated. Shutting down...")