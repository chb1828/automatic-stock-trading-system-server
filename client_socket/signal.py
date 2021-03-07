import json
from datetime import datetime
from asgiref.sync import async_to_sync
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.signals import post_save
from django.dispatch import receiver
from crawler.models import Classification
from channels.layers import get_channel_layer

current_rank_data = None

# 추천 테이블에 값이 save 되면 자동으로 호출된다. 다만, update_or_create 함수를 호출하면 계속 호출된다. update_or_create 내부에 save를 호출하는 코드가 있어 그런것 같다...
@receiver(post_save, sender=Classification)
def send_signal(sender, **kwargs):

    print("socket signal 실행")
    try:
        # 참고 https://stackoverflow.com/questions/21925671/how-to-convert-django-model-object-to-dict-with-its-fields-and-values
        recommendation = Classification.objects.filter(ranked_date=str(datetime.today().strftime('%Y-%m-%d'))).values()[0]
    except Exception as e:
        print(e)
        return

    global current_rank_data
    data = json.dumps(recommendation, cls=DjangoJSONEncoder, ensure_ascii=False)
    if current_rank_data != data:               # 랭킹 데이터를 저장해놓고 이전과 같지 않으면 연결되어있는 client에 랭킹 데이터를 전송한다.
        current_rank_data = data
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




