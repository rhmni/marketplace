from django.contrib import admin
from django.urls import path, include, re_path

from DrfShop.yasg import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('app_account.urls', namespace='account')),
    path('product/', include('app_product.urls', namespace='product')),
    path('store/', include('app_store.urls', namespace='store')),
    path('ticket/', include('app_ticket.urls', namespace='ticket')),
    path('cart/', include('app_cart.urls', namespace='cart')),
    path('order/', include('app_order.urls', namespace='order')),
    path('bookmark/', include('app_bookmark.urls', namespace='bookmark')),

    # for doc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
