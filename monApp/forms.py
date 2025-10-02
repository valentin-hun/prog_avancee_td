from monApp.models import *
from django import forms
from django.forms import BaseModelForm

class ContactUsForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        #fields = '__all__'
        exclude = ('categorie', 'status')