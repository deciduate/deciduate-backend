from django.contrib import admin
from django.urls import path, include
from users.views import *

urlpatterns = [
    path("admin/", admin.site.urls), #관리자 페이지에 접근하기 위한 router

    path('api/v1/users/', include('allauth.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
    
    path('api/v1/users/requirements/', include('requirement.urls')),
    path('api/v1/users/profiles/', include('profiles.urls', namespace='profiles')),
    path('api/v1/users/results/', include('results.urls'))
]
