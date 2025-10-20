from django.db import models

class Profile(models.Model):
    business_name = models.CharField(max_length=100)
    bio = models.TextField()

class Link(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=100)
    url = models.URLField()