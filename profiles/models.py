from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_name = models.CharField(max_length=100)
    bio = models.TextField()
    theme = models.CharField(
    max_length=50,
    default="light",
    choices=[
        ("light", "Light"),
        ("dark", "Dark"),
        ("cupcake", "Cupcake"),
        ("forest", "Forest"),
        ("dracula", "Dracula"),
        ("cyberpunk", "Cyberpunk"),
        ("synthwave", "Synthwave"),
        ("retro", "Retro"),
    ],
    )

class Link(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=100)
    url = models.URLField()