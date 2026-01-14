from django.shortcuts import render ,redirect
from .models import *
from Service.models import *
from django.db.models import Q

# Create your views here.

def get_all_formations(request) : 
    servicegerant = ServiceGerant.objects.filter(user__id =request.user.id ).first()
    user = User.objects.get(id = request.user.id)
    subordonee = user.subordonnee
    subordone= [i.user for i in subordonee]
    print(subordonee)
    serviceformations = Formation.objects.filter( Q(cible_service = servicegerant.service) | Q(cible_user__in = subordone ) )
    formations = [i for i in serviceformations if i.get_statut in ['disponible']]
    print(formations)
   
    myformations = Formation.objects.filter( cible_user__id = request.user.id )
    myformations = [i for i in myformations if i.get_statut in ['disponible','termine','en_cours']]
    # print('f,l,dol',formations)
    return render(request  , 'formations.html',{'formations': formations , 'myformations' : myformations})
def get_one_formations(request,id) : 
    formation = Formation.objects.get(id = id)
    return render(request  , 'formations_detail.html',{'formation': formation})
def create_demande(request) : 
    if request.method =='POST' :
        titre = request.POST['titre']
        auteur  = request.POST['auteur']
        debut = request.POST['debut']
        fin = request.POST['fin']
        type = request.POST['type']
        objectifs = request.POST['objectifs']
        image = request.FILES['img_path']
        if request.POST.get('cible_user', '') :
            cible_user = request.POST['cible_user'] 
        else   : 
            cible_user = request.user
        formation =Formation.objects.create(
                                            titre = titre,
                                            auteur = auteur,
                                            debut = debut
                                            ,fin = fin,
                                            type = type,
                                            objectifs = objectifs,
                                            img_path = image,
                                            cible_user =cible_user,
                                            cible = "user",
                                            statut = 'en_attente'
                                            )
        if(formation) : 
            return redirect('formations')


    return render(request  , 'formation_create.html' , )

def get_all_demandes(request) : 
    servicegerant = ServiceGerant.objects.filter(user__id =request.user.id ).first()
    user = User.objects.get(id = request.user.id)
    subordonee = user.subordonnee
    subordone= [i.user for i in subordonee]
    print(subordonee)
    serviceformations = Formation.objects.filter( Q(cible_service = servicegerant.service) | Q(cible_user__in = subordone ) )
    demandes = [i for i in serviceformations if i.get_statut in ['en_attente' , 'rejete']]
    mydemande = Formation.objects.filter( cible_user__id = request.user.id )
    mydemandes = [i for i in mydemande if i.get_statut in ['en_attente', 'disponible','rejete']]
    # print(mydemandes)
   
    return render(request  , 'soumissions.html' ,  {
        "demandes": demandes , 
        "mydemandes": mydemandes , 
    })


# ADMIN

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Formation


class FormationCreateView(CreateView):
    model = Formation
    template_name = 'admin/formation_form.html'
    success_url = reverse_lazy('dashbord_admin')

class FormationUpdateView(UpdateView):
    model = Formation
    template_name = 'admin/formation_form.html'
    success_url = reverse_lazy('dashbord_admin')

class FormationDeleteView(DeleteView):
    model = Formation
    template_name = 'admin/formation_confirm_delete.html'
    success_url = reverse_lazy('dashbord_admin')

def valider(request,pk) :
        
        formation = Formation.objects.get(id= pk)
        formation.statut = "valide"
        formation.save()
        return redirect('demandes') 
def rejeter(request,pk) :
        formation = Formation.objects.get(id= pk)
        formation.statut = "rejete"
        formation.save()
        return redirect('demandes') 

def nouvel_version_demande (request,pk) :
        print('ok')
        formation = Formation.objects.get(id= pk)
        
        if request.method== 'POST' :
            print('ok')

            f = Formation.objects.create(
                                             titre = formation.titre,
                                            auteur = formation.auteur,
                                            debut =  request.POST["debut"]
                                            ,fin = request.POST["fin"],
                                            type = formation.type,
                                            objectifs = formation.objectifs,
                                            img_path = formation.img_path,
                                            cible_user =request.user,
                                            cible = "user",
                                            statut = 'en_attente')
            return redirect('demandes')
        return redirect('formation_details', id = formation.id)