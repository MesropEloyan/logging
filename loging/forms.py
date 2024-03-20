from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'quantity', 'price', 'is_active', 'email', 'ip_address', 'gender', 'url']
