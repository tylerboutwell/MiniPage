from django.urls import path

from .views import views, user_views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
]