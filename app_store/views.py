from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_store import serializers
from permissions import IsSeller, IsSellerAndHasStore


class CreateStoreView(APIView):
    """
        check and if user don't have store, create one
    """

    serializer_class = serializers.StoreSerializer

    permission_classes = (
        IsSeller,
    )

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

    def put(self, request):
        self.check_object_permissions(request, request.user)
        srz_data = self.serializer_class(data=request.data, instance=request.user.store, partial=True)
        if srz_data.is_valid(raise_exception=True):
            srz_data.save()
            return Response({'message': 'store updated'})


class RetrieveStoreView(APIView):
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
