from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Avatar # Import your model

DEFAULT_AVATAR_PATHS = [
    "default_avatars/avatar1.png",
]

@receiver(post_save, sender=Profile)
def create_default_avatars(sender, instance, created, **kwargs):
    if not created:
        return

    avatars = []

    for path in DEFAULT_AVATAR_PATHS:
        avatar = Avatar.objects.create(
            profile = instance,
            image = path,
        )
        avatars.append(avatar)

    if avatars:
        instance.avatar = avatars[0]
        instance.save()