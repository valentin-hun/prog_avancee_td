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

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = '__all__'

class StatutForm(forms.ModelForm):
    class Meta:
        model = Statut
        fields = '__all__'

class RayonForm(forms.ModelForm):
    class Meta:
        model = Rayon
        fields = '__all__'

class ContenirForm(forms.ModelForm):
    class Meta:
        model = Contenir
        fields = ['produit', 'Qte']