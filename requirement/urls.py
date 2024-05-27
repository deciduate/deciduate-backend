from django.urls import path

from . import views

urlpatterns = [

    path('show/', views.show_requirements, name='show'),
    path('requirements/',views.requirements, name='requirements'),
]
