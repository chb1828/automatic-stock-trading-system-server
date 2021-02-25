from django.db.models.signals import post_save
from django.dispatch import receiver

from crawler.models import News


@receiver(post_save, sender=News)
def analysis(sender, **kwargs ):
    print("save 호출됨!")


