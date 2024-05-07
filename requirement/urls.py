from django.urls import path
from . import views

urlpatterns = [
    path('show_requirements/', views.show_requirements, name='show_requirements'),
]