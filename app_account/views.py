from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_account.models import User
from app_account.tasks import send_sms_user_register, send_sms_forget_password
from app_account.serializers import UserRegisterSerializer, UserVerificationSerializer, \
    UserVerificationPasswordSerializer, UserForgetSerializer

import redis

from permissions import IsAnonymoused


class UserRegisterView(APIView):
    """
    get user data and send sms for verification phone number
    """
    serializer_class = UserRegisterSerializer
    permission_classes = (
        IsAnonymoused,
    )

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            request.session['phone_register'] = srz_data.validated_data['phone']
            send_sms_user_register.delay(srz_data.validated_data)
            return Response(data={'message': 'sms send.'}, status=status.HTTP_200_OK)


class UserVerificationView(APIView):
    """
    check user otp code and create new user
    """
    serializer_class = UserVerificationSerializer
    permission_classes = (
        IsAnonymoused,
    )

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):

            redis_con = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.PHONE_REGISTER_DB)
            code = srz_data.validated_data['code']
            if redis_con.exists(request.session.get('phone_register', 'no_phone')):
                user_data = redis_con.hgetall(request.session['phone_register'])
                if code == int(user_data.get(b'otp_code')):
                    User.objects.create_user(
                        phone=(request.session['phone_register']),
                        name=(user_data[b'name']).decode("utf-8"),
                        password=(user_data[b'password']).decode("utf-8"),
                    )
                    try:
                        del request.session['phone_number']
                    except KeyError:
                        pass
                    return Response({'message': 'you can login now'}, status=status.HTTP_201_CREATED)
                return Response({'message': 'your code is wrong'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'your code is wrong'}, status=status.HTTP_400_BAD_REQUEST)


class UserForgetPassword(APIView):
    """
        check phone number and if exists in db, send sms
    """
    serializer_class = UserForgetSerializer
    permission_classes = (
        IsAnonymoused,
    )

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            phone = srz_data.validated_data['phone']
            try:
                User.objects.get(phone=phone)
                request.session['phone_forget'] = phone
                send_sms_forget_password.delay(phone)
            except User.DoesNotExist:
                pass
            return Response({'message': 'sms send.'}, status=status.HTTP_200_OK)


class UserVerificationPasswordView(APIView):
    """
    check user otp code and password and change the password if otp code is correct
    """
    serializer_class = UserVerificationPasswordSerializer
    permission_classes = (
        IsAnonymoused,
    )

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):

            redis_con = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.FORGET_PASSWORD_DB)
            data = srz_data.validated_data
            if redis_con.exists(request.session.get('phone_forget', 'no_phone')):
                otp_code = redis_con.get(request.session['phone_forget'])
                if data['code'] == int(otp_code):
                    try:
                        user = User.objects.get(
                            phone=(request.session['phone_forget']),
                        )
                        user.set_password(data['password'])
                        user.save()
                    except User.DoesNotExist:
                        return Response({'message': 'error, this phone number is not exists'},
                                        status=status.HTTP_201_CREATED)
                    try:
                        del request.session['phone_forget']
                    except KeyError:
                        pass
                    return Response({'message': 'your password changed'}, status=status.HTTP_201_CREATED)
                return Response({'message': 'your code is wrong'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'your code is wrong'}, status=status.HTTP_400_BAD_REQUEST)
