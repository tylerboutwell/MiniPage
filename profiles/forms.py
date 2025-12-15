from django import forms

from profiles.models import Profile, Link, Avatar


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        profile = self.instance

        # Limit avatar choices to THIS profile's uploads
        self.fields['avatar'].queryset = profile.avatar_set.all()

    avatar = forms.ModelChoiceField(
        queryset=Avatar.objects.all(),
        required=False,
        empty_label="Choose an avatar",  # replaces "------"
        widget=forms.Select(attrs={
            "class": "select select-bordered w-full"
        })
    )

    new_avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'file-input file-input-bordered w-full'
        }),
        help_text="Upload a new avatar (optional)."
    )

    delete_avatar = forms.BooleanField(
        required=False,
        label="Remove current avatar",
        widget=forms.CheckboxInput(attrs={
            "class": "checkbox"
        })
    )

    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'profile_name': forms.TextInput(attrs={'class': 'p-2 w-full border rounded-lg'}),
            'bio': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg',
                'rows': 4}),
            'theme': forms.Select(attrs={
                'class': 'select select-bordered w-full',
                'id': 'theme-select'
            }),

        }
        help_texts = {
            'avatar': 'Choose an existing avatar from your uploads.'
        }

    def save(self, commit=True):
        profile = super().save(commit=False)

        new_avatar_file = self.cleaned_data.get("new_avatar")

        if new_avatar_file:
            avatar = Avatar.objects.create(
                image=new_avatar_file,
                profile=profile,
            )
            profile.avatar = avatar

        if self.cleaned_data.get("delete_avatar"):
            profile.avatar = None

        if commit:
            profile.save()

        return profile

class LinkForm(forms.ModelForm):
    url = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded-lg',
            'placeholder': 'mywebsite.com'
        })
    )
    class Meta:
        model = Link
        exclude = ['user', 'profile', 'position']
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