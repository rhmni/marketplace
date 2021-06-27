from django.urls import path

from app_product.views import ProductListView, FilterProducByCategoryView

app_name = 'product'
urlpatterns = [
    path('products/', ProductListView.as_view(), name='show_one_product'),
    path('products/<int:product_id>/', ProductListView.as_view(), name='show_list_products'),

    path('category/<slug:category_slug>/', FilterProducByCategoryView.as_view(), name='show_category_filter_product'),
]
