import json
from datetime import datetime
from asgiref.sync import async_to_sync
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.signals import post_save
from django.dispatch import receiver
from crawler.models import News, Recommend
from channels.layers import get_channel_layer

current_data = None

@receiver(post_save, sender=News)
def send_signal(sender, **kwargs):

    try:
        # 참고 https://stackoverflow.com/questions/21925671/how-to-convert-django-model-object-to-dict-with-its-fields-and-values
        recommendation = Recommend.objects.filter(ranked_date=str(datetime.today().strftime('%Y-%m-%d'))).values()[0]
    except Exception as e:
        print(e)
        return

    global current_data
    data = json.dumps(recommendation, cls=DjangoJSONEncoder, ensure_ascii=False)
    if current_data != data:
        current_data = data
        print(type(data))
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "ASTS",
            {
                'type': 'client_notification',
                'data': data
            }
        )
    else:
        return




