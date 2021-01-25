from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.db import models


class Stock(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    code = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=128)
    cnt = models.BigIntegerField()
    construction = models.CharField(max_length=64)
    listedDate = models.DateTimeField()
    lastPrice = models.CharField(max_length=64)
    state = models.CharField(max_length=64)

    class Meta:
        db_table = 'stock'

    def __str__(self):
        return self.name
