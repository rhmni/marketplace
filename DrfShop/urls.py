from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('app_account.urls', namespace='account')),
    path('product/', include('app_product.urls', namespace='product')),
    path('store/', include('app_store.urls', namespace='store')),
    path('ticket/', include('app_ticket.urls', namespace='ticket')),
]
