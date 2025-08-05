from django import forms
from .models import *
class SellerProductForm(forms.ModelForm):
    class Meta:
        model = SellerProduct
        fields = ['name', 'description', 'price', 'quantity', 'image'] 
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }