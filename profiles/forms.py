from django import forms

from profiles.models import Profile, Link


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ['user', 'profile']