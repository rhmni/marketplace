from datetime import datetime

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app_bookmark.models import Bookmark
from app_bookmark.serializers import CreateBookmarkSerializer, ListBookmarkSerializer
from app_product.models import Product


class CreateBookmarkView(GenericAPIView):
    """
        add selected product to bookmark
    """

    serializer_class = CreateBookmarkSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            product_id = srz_data.validated_data['product_id']

            try:
                Bookmark.objects.get(user=request.user, product__id=product_id)
                return Response(data={'message': 'this product already added to your bookmarks'}, status=status.HTTP_400_BAD_REQUEST)

            except Bookmark.DoesNotExist:
                product = Product.objects.get(pk=product_id)
                Bookmark.objects.create(
                    user=request.user,
                    product=product,
                    register_date=datetime.now(),
                )
                return Response(data={'message': 'product added to your bookmarks'}, status=status.HTTP_200_OK)


class ListBookmarkView(GenericAPIView):
    """
        list of bookmarks for user
    """

    serializer_class = ListBookmarkSerializer

    permission_classes = (
        IsAuthenticated,
    )

    def get(self, request):
        products = Bookmark.objects.filter(user=request.user)
        srz_data = self.serializer_class(instance=products, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class DeleteBookmarkView(GenericAPIView):
    """
        delete a product in bookmarks if exists
    """

    permission_classes = (
        IsAuthenticated,
    )

    def delete(self, request, product_id):
        get_object_or_404(Bookmark, product__id=product_id).delete()
        return Response(data={'message': 'product deleted of bookmarks'}, status=status.HTTP_200_OK)
