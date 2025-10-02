from django.urls import path
from . import views

urlpatterns = [
    path("contact_us/", views.ContactView, name="contact_us"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("home/<param>",views.HomeView.as_view(), name='accueil'),
    path("about_us/", views.AboutView.as_view(), name="about_us"),
    path("produits/",views.ProduitListView.as_view(), name="lst_prdts"),
    path("produit/<pk>/",views.ProduitDetailView.as_view(), name="dtl_prdt"),
    path("produit/",views.ProduitCreate, name="crt-prdt"),
    path('categories/',views.CategorieListView.as_view(), name='lst_cats'),
    path("categorie/<pk>/",views.CategorieDetailView.as_view(), name="dtl_cat"),
    path('statuts/',views.StatutListView.as_view(), name='lst_stats'),
    path("statut/<pk>/",views.StatutDetailView.as_view(), name="dtl_stat"),
    path('rayons/',views.RayonListView.as_view(), name='lst_rayons'),
    path("rayon/<pk>/",views.RayonDetailView.as_view(), name="dtl_rayon"),
    path('login/', views.ConnectView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.DisconnectView.as_view(), name='logout'),
    path('home/', views.HomeView.as_view(), name='email-sent'),
    path("produit/<pk>/update/",views.ProduitUpdate, name="prdt-chng"),
    path("produit/<pk>/delete/",views.produit_delete, name="dlt_prdt"),
]