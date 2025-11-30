from django import forms

from profiles.models import Profile, Link


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'profile_name': forms.TextInput(attrs={'class': 'p-2 w-full border rounded-lg'}),
            'bio': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg',
                'rows': 4}),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'file-input file-input-bordered w-full'
            }),
            'theme': forms.Select(attrs={
                'class': 'select select-bordered w-full',
                'id': 'theme-select'
            }),

        }
        help_texts = {
            'avatar': 'Upload a profile image (optional).'
        }

class LinkForm(forms.ModelForm):
    url = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded-lg',
            'placeholder': 'mywebsite.com'
        })
    )
    class Meta:
        model = Link
        exclude = ['user', 'profile']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg',
                                            'placeholder': 'Your website'}),

        }
    def clean_url(self):
        url = self.cleaned_data['url'].strip()

        # If user leaves off http:// or https://, auto-add https://
        if url and not url.startswith(("http://", "https://")):
            url = "https://" + url

        return url