"""option URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
#


schema_view = get_schema_view(
   openapi.Info(
      title="스웨거",
      default_version='v1',
      description="API를 테스트 해볼 수 있습니다.",
      terms_of_service="https://github.com/yih789",
      contact=openapi.Contact(email="yih789@naver.com"),
   ),
   validators=['flex'],
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # django
    path('admin/', admin.site.urls),
    path('serverDev/', include('serverDev.urls')),

    # swagger
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
]
