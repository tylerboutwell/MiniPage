from django.urls import path

from .views import views, user_views

urlpatterns = [
    path("", views.home, name="home"),
]