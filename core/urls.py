from django.urls import path

from .views import views, user_views
from django.contrib.auth import views as auth_views
from .forms import StyledAuthenticationForm

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path('login/', auth_views.LoginView.as_view(authentication_form=StyledAuthenticationForm), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:home'), name="logout"),
    path('register/', user_views.register, name="register"),
    path("<str:username>/", views.minipage_view, name="minipage")
]