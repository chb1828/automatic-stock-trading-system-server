import os
from multiprocessing import Process, Queue
from django.apps import AppConfig
from analyzer import analysisProcess
import atexit


class ApiConfig(AppConfig):
    name = 'api'