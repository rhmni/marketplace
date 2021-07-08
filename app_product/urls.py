from django.urls import path

from app_product import views

app_name = 'products'
urlpatterns = [
    # get 1 or list of products
    path('p/', views.ProductListView.as_view(), name='show_one_product'),
    path('p/<product_id>/', views.ProductListView.as_view(), name='show_list_products'),

    # get products by category
    path('categories/<slug:category_slug>/', views.FilterProducByCategoryView.as_view(), name='show_category_filter_product'),

    # show list of categories
    path('categories/', views.CategoryListView.as_view(), name='show_categories'),

    # get, create, update, delete product for seller user
    path('', views.ProfileProductListView.as_view(), name='list_of_product'),
    path('create/', views.CreateProductView.as_view(), name='create_product'),
    path('update/<int:product_id>/', views.UpdateProductView.as_view(), name='update_product'),
    path('delete/<int:product_id>/', views.DeleteProductView.as_view(), name='delete_product'),
]
