from django.urls import path

from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('create/', views.create_profile, name='create_profile'),
    path('', views.profile_detail, name='profile_detail'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('links/add/', views.add_link, name='add_link'),
    path('links/<int:link_id>/edit/', views.edit_link, name='edit_link'),
    path('links/<int:link_id>/delete/', views.delete_link, name='delete_link'),
    path("links/<int:link_id>/row/", views.link_row, name="link_row"),
    path("links/reorder/", views.reorder_links, name="reorder_links"),
]