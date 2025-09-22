from django.urls import path
from . import views

urlpatterns = [
    # path("about_us/", views.about_us, name="about_us"),
    path("contact_us/", views.ContactView.as_view(), name="contact_us"),
    # path('home/<param>',views.home ,name='home'),
    # path('home/',views.home ,name='home'),
    path("home/", views.HomeView.as_view() ,name="home"),
    path("home/<param>",views.HomeView.as_view() ,name='accueil'),
    path("about_us/", views.AboutView.as_view() ,name="about_us"),
    path('produits/',views.ListProduits ,name='produits'),
    path('categories/',views.ListCategories ,name='categories'),
    path('statuts/',views.ListStatuts ,name='statuts'),
    path('rayons/',views.ListRayons ,name='rayons')
]