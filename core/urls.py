from django.urls import path

from .views import views, user_views
from django.contrib.auth import views as auth_views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('register/', user_views.register, name="register"),
]