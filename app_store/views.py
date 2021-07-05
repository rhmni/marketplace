from datetime import datetime

from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from app_store import serializers
from app_store.models import StoreCheckout
from app_store.serializers import StoreCheckoutSerializer, CretaeStoreCheckoutSerializer
from permissions import IsSeller, IsSellerAndHasStore


class CreateStoreView(APIView):
    """
        check and if user don't have store, create one
    """

    serializer_class = serializers.StoreSerializer

    permission_classes = (
        IsSeller,
    )

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        self.check_object_permissions(request, request.user)
        try:
            store = request.user.store
            return Response({'message': 'you already create a store'})
        except:

            srz_data = self.serializer_class(data=request.data)
            if srz_data.is_valid(raise_exception=True):
                srz_data.save(
                    founder=request.user,
                )

                return Response({'message': 'store created'})


class UpdateStoreView(APIView):
    """
        check and if user have store update it
    """

    serializer_class = serializers.StoreSerializer

    permission_classes = (
        IsSellerAndHasStore,
    )

    @swagger_auto_schema(request_body=serializer_class)
    def put(self, request):
        self.check_object_permissions(request, request.user)
        srz_data = self.serializer_class(data=request.data, instance=request.user.store, partial=True)
        if srz_data.is_valid(raise_exception=True):
            srz_data.save()
            return Response({'message': 'store updated'})


class RetrieveStoreView(GenericAPIView):
    """
        check and if user have store retrieve it
    """

    serializer_class = serializers.StoreSerializer

    permission_classes = (
        IsSellerAndHasStore,
    )

    def get(self, request):
        self.check_object_permissions(request, request.user)
        srz_data = self.serializer_class(instance=request.user.store)
        return Response(srz_data.data, status=status.HTTP_200_OK)


class StoreCheckoutView(APIView):
    """
        create checkout for store
    """

    serializer_class = CretaeStoreCheckoutSerializer

    permission_classes = (
        IsSellerAndHasStore,
    )

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        self.check_object_permissions(request, request.user)
        srz_data = self.serializer_class(data=request.data)

        if srz_data.is_valid(raise_exception=True):
            data = srz_data.validated_data
            store = request.user.store

            if settings.MIN_CHECKOUT > store.wallet:
                return Response(
                    {
                        'message': f'amount of your wallet store must more or equal than {settings.MIN_CHECKOUT} toman, it is {store.wallet}'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif data['amount'] > store.wallet:
                return Response(
                    {'message': f'your amount must be less or equal your wallet it is {store.wallet} toman'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            StoreCheckout.objects.create(
                store=store,
                pay_date=datetime.now(),
                amount=data['amount'],
                bank_number=data.get('bank_number'),
            )
            return Response({'message': 'checkout success.'}, status=status.HTTP_200_OK)


class RetrieveStoreCheckout(GenericAPIView):
    """
        retrieve list of checkout for store
    """

    serializer_class = StoreCheckoutSerializer

    permission_classes = (
        IsSellerAndHasStore,
    )

    def get(self, request):
        self.check_object_permissions(request, request.user)
        checkouts = StoreCheckout.objects.filter(store=request.user.store)
        srz_data = self.serializer_class(instance=checkouts, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)
