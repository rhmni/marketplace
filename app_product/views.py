from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app_product.models import Product
from app_product.serializers import ProductSerializer


class ProductListView(APIView):
    """
    get 1 or list of products for show to users
    """
    serializer_class = ProductSerializer
    permission_classes = (
        AllowAny,
    )

    def get(self, request, product_id=None):
        if product_id is not None:
            product = get_object_or_404(Product.confirmed, pk=product_id)
            srz_data = self.serializer_class(instance=product)
            return Response(data=srz_data.data, status=status.HTTP_200_OK)

        products = Product.confirmed.all()
        srz_data = self.serializer_class(instance=products, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class FilterProducByCategoryView(APIView):
    """
    get list of products for show to users with special category
    """
    serializer_class = ProductSerializer
    permission_classes = (
        AllowAny,
    )

    def get(self, request, category_slug):
        products = Product.confirmed.filter(category__slug=category_slug)
        srz_data = self.serializer_class(instance=products, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)
