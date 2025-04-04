from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100, label='Vardas')
    email = forms.EmailField(label='El. paštas')
    address = forms.CharField(widget=forms.Textarea, label='Adresas')
    phone = forms.CharField(max_length=20, label='Telefonas (nebūtina)', required=False)

    class ProductImageForm(forms.Form):
        images = forms.FileField(
            widget=forms.ClearableFileInput(attrs={'multiple': True}),
            required=False
    )
        
class MultiImageForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.FileInput(attrs={'multiple': True}),
        required=False
    )

    class Meta:
        model = forms.models.Model  # This will be replaced at runtime; not used directly
        fields = ['images']