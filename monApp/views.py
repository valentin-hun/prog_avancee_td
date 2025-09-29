from django.shortcuts import render
from django.http import HttpResponse, Http404
from monApp.forms import ContactUsForm
from django import forms
from monApp.models import *
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.views.generic import *
from django.core.mail import send_mail
from django.shortcuts import redirect


def accueil(request,param):
    return HttpResponse("<h1>Hello " + param + " ! You're connected</h1>")

class HomeView(TemplateView):
    template_name = "monApp/page_home.html"
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['titreh1'] = "Hello DJANGO"
        if self.kwargs.get('param'):
            context['titreh1'] = "Hello " + self.kwargs.get('param')
        return context

class AboutView(TemplateView):
    template_name = "monApp/page_home.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "About us..."
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name)
    
# class ContactView(TemplateView):
#     template_name = "monApp/page_home.html"
    
def ContactView(request):
    titreh1 = "Contact us !"
    if request.method=='POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MonProjet Contact Us form',
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['admin@monprojet.com'],
            )
            return redirect('email-sent')
    else:
        form = ContactUsForm()
    return render(request, "monApp/page_home.html",{'titreh1':titreh1, 'form':form})
    
class ProduitListView(ListView):
    model = Produit
    template_name = "monApp/list_produits.html"
    context_object_name = "prdts"

    def get_queryset(self):
        return Produit.objects.order_by("prixUnitaireProd")
    
    def get_context_data(self, **kwargs):
        context = super(ProduitListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes produits"
        return context
    
class ProduitDetailView(DetailView):
    model = Produit
    template_name = "monApp/detail_produit.html"
    context_object_name = "prdt"
    
    def get_context_data(self, **kwargs):
        context = super(ProduitDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du produit"
        return context
    
class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        #fields = '__all__'
        exclude = ('categorie', 'status')

def ProduitCreate(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            prdt = form.save()
            return redirect('dtl-prdt', prdt.refProd)
    else:
        form = ProduitForm()
    return render(request, "monApp/create_produit.html", {'form': form})
    
class CategorieListView(ListView):
    model = Categorie
    template_name = "monApp/list_categories.html"
    context_object_name = "cats"
    
    def get_context_data(self, **kwargs):
        context = super(CategorieListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des catégories"
        return context
    
class CategorieDetailView(DetailView):
    model = Categorie
    template_name = "monApp/detail_categorie.html"
    context_object_name = "cat"
    
    def get_context_data(self, **kwargs):
        context = super(CategorieDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail de la catégorie"
        return context
    
class StatutListView(ListView):
    model = Statut
    template_name = "monApp/list_statuts.html"
    context_object_name = "stats"
    
    def get_context_data(self, **kwargs):
        context = super(StatutListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des statuts"
        return context
    
class StatutDetailView(DetailView):
    model = Statut
    template_name = "monApp/detail_statut.html"
    context_object_name = "stat"
    
    def get_context_data(self, **kwargs):
        context = super(StatutDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du statut"
        return context
    
class RayonListView(ListView):
    model = Rayon
    template_name = "monApp/list_rayons.html"
    context_object_name = "rayons"
    
    def get_context_data(self, **kwargs):
        context = super(RayonListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des rayons"
        return context
    
class RayonDetailView(DetailView):
    model = Rayon
    template_name = "monApp/detail_rayon.html"
    context_object_name = "rayon"
    
    def get_context_data(self, **kwargs):
        context = super(RayonDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du rayon"
        return context
    
class ConnectView(LoginView):
    template_name = 'monApp/page_login.html'
    def post(self, request, **kwargs):
        lgn = request.POST.get('username', False)
        pswrd = request.POST.get('password', False)
        user = authenticate(username=lgn, password=pswrd)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'monApp/page_home.html', {'param': lgn, 'message': "You're connected"})
        else:
            return render(request, 'monApp/page_register.html')
        
class RegisterView(TemplateView):
    template_name = 'monApp/page_register.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        mail = request.POST.get('mail', False)
        password = request.POST.get('password', False)
        user = User.objects.create_user(username, mail, password)
        user.save()
        if user is not None and user.is_active:
            return render(request, 'monApp/page_login.html')
        else:
            return render(request, 'monApp/page_register.html')
        
class DisconnectView(TemplateView):
    template_name = 'monApp/page_logout.html'

    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)
    
# Create your views here.

def ListCategories(request):
    cats = Categorie.objects.all()
    return render(request, 'monApp/list_categories.html',{'cats': cats})

def ListStatuts(request):
    stats = Statut.objects.all()
    return render(request, 'monApp/list_statuts.html',{'stats': stats})

def ListRayons(request):
    rayons = Rayon.objects.all()
    return render(request, 'monApp/list_rayons.html',{'rayons': rayons})

def contact_us(request):
    equipe = User.objects.all()
    return render(request, 'monApp/contact_us.html',{'equipe': equipe})

def about_us(request):
    equipe = User.objects.all()
    return render(request, 'monApp/about_us.html', {'equipe': equipe})