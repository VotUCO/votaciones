from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from django.urls import path

urlpatterns = [
    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/token/verify/', TokenVerifyView.as_view(), name='token_verify')
]