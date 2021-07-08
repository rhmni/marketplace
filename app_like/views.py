from datetime import datetime

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app_like.models import Like
from app_like.serialisers import LikeSerializer
from app_product.models import Product


class LikeView(GenericAPIView):
    """
        create a object for like product by user
    """

    serializer_class = LikeSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            product_id = srz_data.validated_data['product_id']
            try:
                Like.objects.get(product__id=product_id, user=request.user)
                return Response({'message': 'this product already liked by you'}, status=status.HTTP_400_BAD_REQUEST)
            except Like.DoesNotExist:
                product = get_object_or_404(Product.confirmed, pk=product_id)
                Like.objects.create(user=request.user, product=product, register_date=datetime.now())
                return Response({'message': 'liked success'}, status=status.HTTP_200_OK)


class DisLikeView(GenericAPIView):
    """
        create a object for like product by user
    """

    serializer_class = LikeSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            product_id = srz_data.validated_data['product_id']
            try:
                Like.objects.get(product__id=product_id, user=request.user).delete()
                return Response({'message': 'like for this produc deleted success'}, status=status.HTTP_200_OK)
            except Like.DoesNotExist:
                return Response({'message': 'you not like this product'}, status=status.HTTP_400_BAD_REQUEST)
