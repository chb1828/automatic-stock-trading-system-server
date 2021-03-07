from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.CrawlingKeyword)
admin.site.register(models.News)
admin.site.register(models.NewsKeyword)
admin.site.register(models.Classification)
