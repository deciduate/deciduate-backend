from django.urls import path
from . import views

urlpatterns = [
    path('api/show_requirements/', views.show_requirements, name='api_show_requirements'),
]