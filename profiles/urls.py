from django.urls import path

from profiles import views

app_name = 'profiles'

urlpatters = [
    path('create/', views.create_profile, name='create_profile'),
]