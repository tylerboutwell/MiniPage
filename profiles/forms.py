from django import forms

from profiles.models import Profile, Link


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'profile_name': forms.TextInput(attrs={'class': 'w-full rounded-lg border border-gray-300 p-2 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'bio': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 4}),

        }

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ['user', 'profile']