from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_name = models.CharField(max_length=100)
    bio = models.TextField()
    ## change this to point to avatar model
    # avatar = models.ImageField(
    #    upload_to='avatars',
    #    blank=True,
    #    null=True,
    #)
    avatar = models.ForeignKey(
        "Avatar",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='selected_avatar',
    )
    theme = models.CharField(
    max_length=50,
    default="light",
    choices=[
        ("light", "Bright"),
        ("dark", "Night"),
        ("cupcake", "Cupcake"),
        ("forest", "Nature"),
        ("dracula", "Dracula"),
        ("cyberpunk", "Retro Wave"),
        ("synthwave", "Neon"),
        ("retro", "Vintage"),
    ],
    )

class Link(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=100)
    url = models.URLField()

class Avatar(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="avatar_set")
    image = models.ImageField(upload_to='avatars')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name.split('/')[-1]