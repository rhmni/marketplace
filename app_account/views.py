from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_account.models import User
from app_account.tasks import send_sms_user_register
from app_account.serializers import UserRegisterSerializer, UserVerificationSerializer

import redis

from permissions import IsAnonymoused


class UserRegisterView(APIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (
        IsAnonymoused,
    )

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            request.session['phone_number'] = srz_data.validated_data['phone']
            send_sms_user_register.delay(srz_data.validated_data)
            return Response(data={'message': 'sms send.'}, status=status.HTTP_200_OK)


class UserVerificationView(APIView):
    serializer_class = UserVerificationSerializer
    permission_classes = (
        IsAnonymoused,
    )

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):

            redis_con = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.PHONE_REGISTER_DB)
            code = srz_data.validated_data['code']
            if redis_con.exists(request.session.get('phone_number', 'no_phone')):
                user_data = redis_con.hgetall(request.session['phone_number'])
                if code == int(user_data.get(b'otp_code')):
                    User.objects.create_user(
                        phone=(request.session['phone_number']),
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
