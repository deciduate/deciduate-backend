from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.InfoView.as_view()), # get
    path('basics/', views.BasicView.as_view()), # get, post, put
    path('completions/', views.CompletionView.as_view()), # get, post
    path('credits/', views.CreditView.as_view()), # get, put
    path('subjects/', views.SubjectView.as_view()), # get, put
    path('extras/', views.ExtraView.as_view()), # get, put
]