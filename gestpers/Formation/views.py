from django.shortcuts import render
from .models import *
from Service.models import *
# Create your views here.

def get_all_formations(request) : 
    servicegerant = ServiceGerant.objects.filter(user__id =request.user.id ).first()
    
    formations = Formation.objects.filter(statut__in = ['en_cours' , 'terminé'] , cible_service__id = servicegerant.service.id)
    return render(request  , 'formations.html',{'formations': formations})

def create_demande(request) : 
    if request.method =='POST' :
        titre = request.POST['titre']
        auteur  = request.POST['auteur ']
        date_debut = request.POST['date_debut']
        date_fin = request.POST['date_fin']
        type = request.POST['type']
        objectifs = request.POST['objectifs']
        image = request.FILES['image']

        
    return render(request  , 'formation_create.html' , )

def get_all_demandes(request) : 
    return render(request  , 'soumissions.html' , )