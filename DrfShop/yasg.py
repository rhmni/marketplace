from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Havij Shop API",
        default_version='v1',
        description="Market Place Store With Django",
        terms_of_service="https://www.rahmanipy.ir/",
        contact=openapi.Contact(email="alirahmani.py@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(
        permissions.AllowAny,
    ),
)