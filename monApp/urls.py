from django.urls import path
from . import views

urlpatterns = [
    path("about_us/", views.about_us, name="about_us"),
    path("contact_us/", views.contact_us, name="contact_us"),
    path('home/<param>',views.home ,name='home'),
    path('home/',views.home ,name='home'),
    path('liste_produits/',views.liste_produits ,name='liste_produits'),
    path('categories/',views.categories ,name='categories'),
    path('statuts/',views.statuts ,name='statuts')
]