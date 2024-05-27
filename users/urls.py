from django.urls import path

from .views import GoogleLoginView, GoogleCallbackView, LogoutView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework import routers

router = routers.DefaultRouter()
# router.register('list', UserViewSet) # 유저리스트 (테스트용)

urlpatterns = [
    path('google/login/', GoogleLoginView.as_view(), name='google_login'),
    path('google/callback/', GoogleCallbackView.as_view(), name='google_callback'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]