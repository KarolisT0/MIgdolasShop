from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Toks el. paštas jau užregistruotas.")
        return email