from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
   path('input/profiles/', views.PostProfile.as_view()),
   path('input/completions/', views.PostCompletion.as_view()),
   path('mypage/profiles', views.PutProfile.as_view()),
   path('mypage/credits', views.PutCredit.as_view()),
   path('mypage/subjects', views.PutSubject.as_view()),
   path('mypage/extras', views.PutExtra.as_view()),
]