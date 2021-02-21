from django.db import models

# Create your models here.

#어차피, 취미프로젝트, 막해, 시발, 설계하다가, 짜증만나지

#검색 키워드....크롤링 키워드에 들어간 항목들에 대해서 뉴스 api를 긁는다.
class CrawlingKeyword(models.Model):
    objects = models.Manager()#dummy property that improves vs code intelligence
    keyword = models.CharField('keyword to search in naver news api', max_length=128, primary_key=True)


#신문사 url(네이버가 아닌 뉴스사의 것을 그대로 가져온다)
#마지막 확인 일자(크롤러가 접근한 일자를 나타내야 한다.)
#제목, 아마도 사람에게는 제목을 보여주는 편이 나을 것이다.
#본문 내용
class News(models.Model):
    objects = models.Manager()
    url = models.URLField('url of news provider', max_length=1024, primary_key=True)
    crawled_date = models.DateTimeField('crawled date')
    posted_date = models.DateTimeField('posted_date')
    head_text = models.TextField('head text')
    body_text = models.TextField('body text of news')


class NewsKeyword(models.Model):
    objects = models.Manager()
    class Meta:
        unique_together = (('url', 'keyword'))
    url = models.URLField('url of news provider', max_length=1024)
    keyword = models.CharField('keyword to search in naver news api', max_length=128)