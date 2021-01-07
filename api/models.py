from django.db import models

class Stock(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    cnt = models.BigIntegerField()
    construction = models.CharField(max_length=20)
    listedDate = models.DateTimeField()
    lastPrice = models.CharField(max_length=10)
    state = models.CharField(max_length=20)

    class Meta:
        db_table = 'stock'

    def __str__(self):
        return self.name