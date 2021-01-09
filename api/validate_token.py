from django.http import HttpResponse
from rest_framework.exceptions import ValidationError


def validate_token(value):
    if(value != "ff35885ab6c63290ccdf60b80a9b37769e287ec5"):
        msg = "토큰값이 잘못 되었습니다"
        raise ValidationError(msg)