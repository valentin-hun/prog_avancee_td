from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from monApp.forms import *
from monApp.models import *
from django.db.models import Count, Prefetch
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator


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
        query = self.request.GET.get('search')
        if query:
            return Produit.objects.filter(intituleProd__icontains=query).select_related('categorie').select_related('status')
        return Produit.objects.select_related('categorie').select_related('status')
    
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

@login_required
def ProduitCreate(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            prdt = form.save()
            return redirect('dtl_prdt', prdt.refProd)
    else:
        form = ProduitForm()
    return render(request, "monApp/create_produit.html", {'form': form})

@login_required
def ProduitUpdate(request, pk):
    prdt = Produit.objects.get(refProd=pk)
    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=prdt)
        if form.is_valid():
            # mettre à jour le produit existant dans la base de données
            form.save()
            # rediriger vers la page détaillée du produit que nous venons de mettre à jour
            return redirect('dtl_prdt', prdt.refProd)
    else:
        form = ProduitForm(instance=prdt)
    return render(request,'monApp/update_produit.html', {'form': form})

# class ProduitDeleteView(DeleteView):
#     model = Produit
#     template_name = "monApp/delete_produit.html"
#     success_url = reverse_lazy('lst_prdts')

@login_required
def ProduitDelete(request, pk):
    prdt = Produit.objects.get(refProd=pk) # nécessaire pour GET et pour POST
    if request.method == 'POST':
        # supprimer le produit de la base de données
        prdt.delete()
        # rediriger vers la liste des produit
        return redirect('lst_prdts')
    # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement
    return render(request, 'monApp/delete_produit.html', {'object': prdt})

@login_required
def CategorieCreate(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            cat = form.save()
            return redirect('dtl_cat', cat.idCat)
    else:
        form = CategorieForm()
    return render(request, "monApp/create_categorie.html", {'form': form})
    
class CategorieListView(ListView):
    model = Categorie
    template_name = "monApp/list_categories.html"
    context_object_name = "cats"

    def get_queryset(self):    
        query = self.request.GET.get('search')
        if query:
            return Categorie.objects.filter(nomCat__icontains=query).annotate(nb_produits=Count('produits_categorie'))
        return Categorie.objects.annotate(nb_produits=Count('produits_categorie'))
    
    def get_context_data(self, **kwargs):
        context = super(CategorieListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes catégories"
        return context
    
class CategorieDetailView(DetailView):
    model = Categorie
    template_name = "monApp/detail_categorie.html"
    context_object_name = "cat"

    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        return Categorie.objects.annotate(nb_produits=Count('produits_categorie'))
    
    def get_context_data(self, **kwargs):
        context = super(CategorieDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail de la catégorie"
        context['prdts'] = self.object.produits_categorie.all()
        return context
    
@login_required    
def CategorieUpdate(request, pk):
    cat = Categorie.objects.get(idCat=pk)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=cat)
        if form.is_valid():
            # mettre à jour le produit existant dans la base de données
            form.save()
            # rediriger vers la page détaillée du produit que nous venons de mettre à jour
            return redirect('dtl_cat', cat.idCat)
    else:
        form = CategorieForm(instance=cat)
    return render(request,'monApp/update_categorie.html', {'form': form})

@login_required
def CategorieDelete(request, pk):
    cat = Categorie.objects.get(idCat=pk) # nécessaire pour GET et pour POST
    if request.method == 'POST':
        # supprimer le produit de la base de données
        cat.delete()
        # rediriger vers la liste des produit
        return redirect('lst_cats')
    # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement
    return render(request, 'monApp/delete_categorie.html', {'object': cat})

@login_required
def StatutCreate(request):
    if request.method == 'POST':
        form = StatutForm(request.POST)
        if form.is_valid():
            stat = form.save()
            return redirect('dtl_stat', stat.idStatus)
    else:
        form = StatutForm()
    return render(request, "monApp/create_statut.html", {'form': form})
    
class StatutListView(ListView):
    model = Statut
    template_name = "monApp/list_statuts.html"
    context_object_name = "stats"

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return Statut.objects.filter(libelleStatus__icontains=query).annotate(nb_produits=Count('produits_status'))
        return Statut.objects.annotate(nb_produits=Count('produits_status'))
    
    def get_context_data(self, **kwargs):
        context = super(StatutListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des statuts"
        return context
    
class StatutDetailView(DetailView):
    model = Statut
    template_name = "monApp/detail_statut.html"
    context_object_name = "stat"

    def get_queryset(self):
        return Statut.objects.annotate(nb_produits=Count('produits_status'))
    
    def get_context_data(self, **kwargs):
        context = super(StatutDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du statut"
        context['prdts'] = self.object.produits_status.all()
        return context
    
@login_required
def StatutUpdate(request, pk):
    stat = Statut.objects.get(idStatus=pk)
    if request.method == 'POST':
        form = StatutForm(request.POST, instance=stat)
        if form.is_valid():
            # mettre à jour le produit existant dans la base de données
            form.save()
            # rediriger vers la page détaillée du produit que nous venons de mettre à jour
            return redirect('dtl_stat', stat.idStatus)
    else:
        form = StatutForm(instance=stat)
    return render(request,'monApp/update_statut.html', {'form': form})

@login_required
def StatutDelete(request, pk):
    stat = Statut.objects.get(idStatus=pk) # nécessaire pour GET et pour POST
    if request.method == 'POST':
        # supprimer le produit de la base de données
        stat.delete()
        # rediriger vers la liste des produit
        return redirect('lst_stats')
    # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement
    return render(request, 'monApp/delete_statut.html', {'object': stat})

@login_required
def RayonCreate(request):
    if request.method == 'POST':
        form = RayonForm(request.POST)
        if form.is_valid():
            rayon = form.save()
            return redirect('dtl_rayon', rayon.idRayon)
    else:
        form = RayonForm()
    return render(request, "monApp/create_rayon.html", {'form': form})
    
class RayonListView(ListView):
    model = Rayon
    template_name = "monApp/list_rayons.html"
    context_object_name = "rayons"

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return Rayon.objects.filter(nomRayon__icontains=query).prefetch_related(Prefetch("contenir_rayon", queryset=Contenir.objects.select_related("produit")))
        # Précharge tous les "contenir" de chaque rayon,
        # et en même temps le produit de chaque contenir
        return Rayon.objects.prefetch_related(Prefetch("contenir_rayon", queryset=Contenir.objects.select_related("produit")))
    
    def get_context_data(self, **kwargs):
        context = super(RayonListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des rayons"
        ryns_dt = []
        for rayon in context['rayons']:
            total = 0
            for contenir in rayon.contenir_rayon.all():
                total += contenir.produit.prixUnitaireProd * contenir.Qte
            ryns_dt.append({'rayon': rayon,'total_stock': total})
        context['ryns_dt'] = ryns_dt
        return context
    
class RayonDetailView(DetailView):
    model = Rayon
    template_name = "monApp/detail_rayon.html"
    context_object_name = "rayon"
    
    def get_context_data(self, **kwargs):
        context = super(RayonDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du rayon"
        prdts_dt = []
        total_rayon = 0
        total_nb_produit = 0
        for contenir in self.object.contenir_rayon.all():
            total_produit = contenir.produit.prixUnitaireProd * contenir.Qte
            prdts_dt.append({'produit': contenir.produit,
                             'qte': contenir.Qte,'prix_unitaire': contenir.produit.prixUnitaireProd,
                             'total_produit': total_produit
                            })
            total_rayon += total_produit
            total_nb_produit += contenir.Qte
        context['prdts_dt'] = prdts_dt
        context['total_rayon'] = total_rayon
        context['total_nb_produit'] = total_nb_produit
        return context
    
@login_required
def RayonUpdate(request, pk):
    rayon = Rayon.objects.get(idRayon=pk)
    if request.method == 'POST':
        form = RayonForm(request.POST, instance=rayon)
        if form.is_valid():
            # mettre à jour le produit existant dans la base de données
            form.save()
            # rediriger vers la page détaillée du produit que nous venons de mettre à jour
            return redirect('dtl_rayon', rayon.idRayon)
    else:
        form = RayonForm(instance=rayon)
    return render(request,'monApp/update_rayon.html', {'form': form})

@login_required
def RayonDelete(request, pk):
    rayon = Rayon.objects.get(idRayon=pk) # nécessaire pour GET et pour POST
    if request.method == 'POST':
        # supprimer le produit de la base de données
        rayon.delete()
        # rediriger vers la liste des produit
        return redirect('lst_rayons')
    # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement
    return render(request, 'monApp/delete_rayon.html', {'object': rayon})

class ContenirCreateView(CreateView):
    model = Contenir
    form_class = ContenirForm
    template_name = "monApp/create_contenir.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        pdrt = Contenir.objects.get(Produit)
        if form.is_valid():
            rayon = form.save()
            return redirect('cntnr-crt', rayon.idRayon)
    
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