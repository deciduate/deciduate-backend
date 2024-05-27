from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('requirement.urls')),
    path('api/v1/users/', include('profiles.urls', namespace='profiles')),
    path('api/v1/users/results/', include('results.urls'))
]