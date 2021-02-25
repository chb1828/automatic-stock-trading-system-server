from datetime import datetime

from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from crawler.models import News, Recommend
from channels.layers import get_channel_layer
from django.core import serializers


@receiver(post_save, sender=News)
def send_signal(sender, **kwargs):

    print(datetime.today().strftime('%Y-%m-%d'),"찍힘")
    recommendation = Recommend.objects.get(ranked_date=str(datetime.today().strftime('%Y-%m-%d')))
    data = "123"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "ASTS",
        {
            'type': 'client_notification',
            'data': data
        }
    )


