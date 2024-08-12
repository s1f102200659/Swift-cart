from django import forms
from .models import Product

class UploadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image']