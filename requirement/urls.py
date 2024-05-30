from django.urls import path

from . import views


urlpatterns = [
    path('requirements/show/', views.show_requirements, name='show'),
    path('requirements/',views.RequirementView.as_view(), name='requirements'),
]
