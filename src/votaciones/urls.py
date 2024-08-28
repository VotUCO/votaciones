"""
URL configuration for votaciones project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from src.votaciones.settings import VERSION

schema_view = get_schema_view(
    openapi.Info(
        title="Documentación API Votaciones (VotUCO spec)",
        default_version="v1",
        description="Docs for VotUCO API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="jesusescribano2002@gmail.com"),
        license=openapi.License(name="Apache License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redocs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(f"api/{VERSION}/voting/", include("src.voting.infrastructure.router")),
    path(f"api/{VERSION}/user/", include("src.users.infrastructure.router")),
]
