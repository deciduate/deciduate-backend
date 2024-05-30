from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('<int:pk>', views.InfoView.as_view()), # get
    path('basics/<int:pk>', views.BasicView.as_view()), # get, post, put
    path('completions/', views.CompletionView.as_view()), # get, post
    path('credits/<int:pk>', views.CreditView.as_view()), # get, put
    path('subjects/<int:pk>', views.SubjectView.as_view()), # get, put
    path('extras/<int:pk>', views.ExtraView.as_view()), # get, put
]