from django import forms
from django import forms
from .models import ProductImage  # ✅ Make sure this is imported

# 🛒 Checkout form (good as-is)
class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100, label='Vardas')
    email = forms.EmailField(label='El. paštas')
    address = forms.CharField(widget=forms.Textarea, label='Adresas')
    phone = forms.CharField(max_length=20, label='Telefonas (nebūtina)', required=False)

# 🖼️ Product image form with multiple upload
class ProductImageForm(forms.Form):
    images = forms.FileField(
        widget=forms.FileInput(attrs={'multiple': True}),
        required=False
    )

# ✅ Model form for inline in admin (tied to ProductImage)
class MultiImageForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False
    )

    class Meta:
        model = ProductImage  # 🔄 Link it properly to the model
        fields = ['image']
