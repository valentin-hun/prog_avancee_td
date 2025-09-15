from django.db import models
from django.utils import timezone

# Create your models here.

class Categorie(models.Model):
    idCat = models.AutoField(primary_key=True)
    nomCat = models.CharField(max_length=100)

    def __str__(self):
        return self.nomCat

class Produit(models.Model):
    refProd = models.AutoField(primary_key=True)
    intituleProd = models.CharField(max_length=200)
    prixUnitaireProd = models.DecimalField(max_digits=10, decimal_places=2)
    # Relation CIF : chaque produit appartient à 1 catégorie (0,N côté catégorie → 1,1 côté produit)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="produits",null=True, blank=True)

    date_fab = models.DateField(default=timezone.now)

    def __str__(self):
        return self.intituleProd
    
class Rayon(models.Model):
    idRayon = models.AutoField(primary_key=True)
    nomRayon = models.CharField(max_length=100)

    def __str__(self):
        return self.nomRayon

class Contenir(models.Model):
    idRayon = models.ForeignKey(Rayon, on_delete=models.CASCADE, related_name="contient")
    refProd = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="contient")
    qte = models.IntegerField()

    def __str__(self):
        return "(" + self.idRayon + "," + self.refProd + "," + self.quantite + ")"
    
class Statut(models.Model):
    idStatut = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=100)
    
    def __str__(self):
        return self.libelle