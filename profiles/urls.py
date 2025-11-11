from django.urls import path

from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('create/', views.create_profile, name='create_profile'),
    path('<int:profile_id>', views.profile_detail, name='profile_detail'),
    path('<int:profile_id>/edit', views.edit_profile, name='edit_profile'),
    #path('<int:profile_id>/links/add', views.add_link, name='add_link'),
    #path('<int:profile_id>/links/<int:link_id>/edit', views.edit_link, name='edit_link'),
    #path('<int:profile_id>/links/<int:link_id>/delete', views.delete_link, name='delete_link'),
]