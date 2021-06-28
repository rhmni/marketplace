import redis
from celery import shared_task
from kavenegar import *

from random import randint

from django.conf import settings


@shared_task
def send_sms_user_register(data):
    redis_con = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.PHONE_REGISTER_DB)
    otp_code = randint(100000, 999999)
    user = {
        'otp_code': otp_code,
        'name': data['name'],
        'password': data['password'],
    }
    redis_con.hmset(data['phone'], user)
    redis_con.expire(data['phone'], settings.TIME_EXPIRE)
    api = KavenegarAPI(
        settings.KAVENEGAR_SECRET_KEY
    )
    params = {
        'sender': '',
        'receptor': data['phone'],
        'message': f'your code is {otp_code} , time is {settings.TIME_EXPIRE} seconds',
    }
    response = api.sms_send(params)


@shared_task
def send_sms_forget_password(phone):
    redis_con = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.FORGET_PASSWORD_DB)
    otp_code = randint(100000, 999999)

    redis_con.set(phone, otp_code, settings.TIME_EXPIRE)

    api = KavenegarAPI(
        settings.KAVENEGAR_SECRET_KEY
    )
    params = {
        'sender': '',
        'receptor': phone,
        'message': f'your code is {otp_code} , time is {settings.TIME_EXPIRE} seconds',
    }
    print(otp_code)
    response = api.sms_send(params)
