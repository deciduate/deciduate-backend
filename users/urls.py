from django.urls import path

from .views import GoogleLoginView, GoogleCallbackView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('google/login/', GoogleLoginView.as_view(), name='google_login'),
    path('google/callback/', GoogleCallbackView.as_view(), name='google_callback'),
    path('logout/', LogoutView.as_view(), name='logout'),
]