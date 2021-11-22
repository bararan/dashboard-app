from django.urls import path
from .views import own_profile_view

app_name = 'profiles'

urlpatterns = [
    path('', own_profile_view, name='own_profile')
]