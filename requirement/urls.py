from django.urls import path

from . import views


urlpatterns = [
    path('show/', views.show_requirements, name='show'),
    path('',views.RequirementView.as_view(), name='requirements'),
]
