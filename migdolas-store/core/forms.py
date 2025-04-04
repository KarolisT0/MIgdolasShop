from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100, label='Vardas')
    email = forms.EmailField(label='El. paštas')
    address = forms.CharField(widget=forms.Textarea, label='Adresas')
    phone = forms.CharField(max_length=20, label='Telefonas (nebūtina)', required=False)