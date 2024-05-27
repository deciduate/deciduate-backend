from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls), #관리자 페이지에 접근하기 위한 router
    path('api-auth/',include('rest_framework.urls')),
    path('api/v1/requirement/', include('requirement.urls')),
    path('api/v1/users/', include('requirement.urls')),
]