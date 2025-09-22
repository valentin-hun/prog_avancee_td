from django.urls import path
from . import views

urlpatterns = [
    path("contact_us/", views.ContactView.as_view(), name="contact_us"),
    path("home/", views.HomeView.as_view() ,name="home"),
    path("home/<param>",views.HomeView.as_view() ,name='accueil'),
    path("about_us/", views.AboutView.as_view() ,name="about_us"),
    path("produits/",views.ProduitListView.as_view()),
    path("produit/<pk>/",views.ProduitDetailView.as_view()),
    path('categories/',views.ListCategories ,name='categories'),
    path('statuts/',views.ListStatuts ,name='statuts'),
    path('rayons/',views.ListRayons ,name='rayons')
]