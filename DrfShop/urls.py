from django.contrib import admin
from django.urls import path, include, re_path

from DrfShop.yasg import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('app_account.urls', namespace='account')),
    path('products/', include('app_product.urls', namespace='product')),
    path('stores/', include('app_store.urls', namespace='store')),
    path('tickets/', include('app_ticket.urls', namespace='ticket')),
    path('carts/', include('app_cart.urls', namespace='cart')),
    path('orders/', include('app_order.urls', namespace='order')),
    path('bookmarks/', include('app_bookmark.urls', namespace='bookmark')),
    path('likes/', include('app_like.urls', namespace='likes')),

    # for doc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
