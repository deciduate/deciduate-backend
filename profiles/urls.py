from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.InfoView.as_view()),
    path('basics/', views.BasicView.as_view()),
    path('completions/', views.CompletionView.as_view()),
    path('credits/', views.CreditView.as_view()),
    path('subjects/', views.SubjectView.as_view()),
    path('extras/', views.ExtraView.as_view()),
]