from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import UserProfile

# 🛒 Checkout form
class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100, label='Vardas')
    email = forms.EmailField(label='El. paštas')
    address = forms.CharField(widget=forms.Textarea, label='Adresas')
    phone = forms.CharField(max_length=20, label='Telefonas (nebūtina)', required=False)

# authentication form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='El. paštas')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            'username': 'Vartotojo vardas',
            'email': 'El. paštas',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Slaptažodis'
        self.fields['password2'].label = 'Pakartoti slaptažodį'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Toks el. paštas jau užregistruotas.")
        return email
    

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Vartotojo vardas",
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    password = forms.CharField(
        label="Slaptazodis",
        widget=forms.TextInput(attrs={'autofocus': True})
    )

# Profile form

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='Vardas', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, label='Pavardė', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['phone', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }