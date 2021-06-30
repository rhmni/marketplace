from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app_product.serializers import ProfileProductSerializer
from app_product.models import Product
from app_product.serializers import ProductGetSerializer
from permissions import IsSeller, IsSellerOfProduct, IsSellerAndHasStore


class ProductListView(APIView):
    """
        get 1 or list of products for show to users
    """

    serializer_class = ProductGetSerializer
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

    serializer_class = ProductGetSerializer
    permission_classes = (
        AllowAny,
    )

    def get(self, request, category_slug):
        products = Product.confirmed.filter(category__slug=category_slug)
        srz_data = self.serializer_class(instance=products, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class CreateProductView(APIView):
    """
        check if user have store, create new product
    """

    serializer_class = ProfileProductSerializer

    permission_classes = (
        IsSellerAndHasStore,
    )

    def post(self, request):
        self.check_object_permissions(request, request.user)

        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            srz_data.save(
                seller=request.user.store,
            )
            return Response({'message': 'product created.'}, status=status.HTTP_201_CREATED)


class UpdateProductView(APIView):
    """
        check user is seller of product and update it
    """

    serializer_class = ProfileProductSerializer

    permission_classes = (
        IsSellerOfProduct,
    )

    def put(self, request, product_id):
        product = get_object_or_404(Product.confirmed, pk=product_id)
        self.check_object_permissions(request, product)
        srz_data = self.serializer_class(data=request.data, instance=product, partial=True)
        if srz_data.is_valid(raise_exception=True):
            srz_data.save()
            product.is_confirm = False
            product.save()
            return Response(data=srz_data.data, status=status.HTTP_204_NO_CONTENT)


class DeleteProductView(APIView):
    """
        check user is seller of product and delete it
    """
    permission_classes = (
        IsSellerOfProduct,
    )

    def delete(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        self.check_object_permissions(request, product)
        product.delete()
        return Response({'message': 'product deleted.'}, status=status.HTTP_200_OK)


class ProfileProductListView(APIView):
    """
        list of products for seller user
    """

    serializer_class = ProfileProductSerializer

    permission_classes = (
        IsSellerAndHasStore,
    )

    def get(self, request):
        products = request.user.store.products.all()
        srz_data = self.serializer_class(instance=products, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)
