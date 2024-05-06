from django.contrib import admin
from django.urls import path, include
from users.views import *

urlpatterns = [
<<<<<<< HEAD
    path("admin/", admin.site.urls), #관리자 페이지에 접근하기 위한 router

    path('api/v1/users/', include('allauth.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('requirement/', include('requirement.urls')),
]
=======
    path("admin/", admin.site.urls),
    path('', include('requirement.urls')),
]
>>>>>>> 8cd45e1 (Feat : requirement 모델 생성)
