from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Email Address'
        })
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Last Name'
        })
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        input_classes = "w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"

        self.fields["username"].widget.attrs.update({
            "class": input_classes,
            "placeholder": "Username"
        })
        self.fields["username"].label = ""

        self.fields["password1"].widget.attrs.update({
            "class": input_classes,
            "placeholder": "Password"
        })
        self.fields["password1"].label = ""

        self.fields["password2"].widget.attrs.update({
            "class": input_classes,
            "placeholder": "Confirm Password"
        })
        self.fields["password2"].label = ""

class StyledAuthenticationForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		cls = "w-full p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
		# Update widget attrs
		self.fields['username'].widget.attrs.update({'class': cls, 'placeholder': 'Username'})
		self.fields['password'].widget.attrs.update(
			{'class': cls, 'placeholder': 'Password', 'autocomplete': 'current-password'})