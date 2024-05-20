from django.contrib import admin
from django.urls import path, include

urlpatterns = [
<<<<<<< HEAD
    path("admin/", admin.site.urls), #관리자 페이지에 접근하기 위한 router
    path('api-auth/',include('rest_framework.urls')),
    path('requirement/', include('requirement.urls')),
=======
    path("admin/", admin.site.urls),
    path('', include('requirement.urls')),
>>>>>>> 202201617-feature/profile
]