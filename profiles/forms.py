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
    url = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'mywebsite.com'
        })
    )
    class Meta:
        model = Link
        exclude = ['user', 'profile']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full rounded-lg border border-gray-300 p-2 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                                            'placeholder': 'Your website'}),

        }
    def clean_url(self):
        url = self.cleaned_data['url'].strip()

        # If user leaves off http:// or https://, auto-add https://
        if url and not url.startswith(("http://", "https://")):
            url = "https://" + url

        return url