from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import  LogoutView
from .form import *
# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def home(request) :
    return render(request , 'home.html')


# views.py


def register(request):
    form = inscriptionForm()
    if request.method == 'POST':
        form = inscriptionForm(request.POST)
        if(form.is_valid()):
        
            form.save()
            messages.success(request, f"Compte Creeé, ")
            return redirect('login')

        else:
                    messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
       
    
                
    return render(request, 'register.html', {"form" : form})


def connexion_view(request):
    if request.method == 'POST':
        
            # Récupération des données nettoyées
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(email , password)
            myuser = User.objects.filter(email=email).first()  
            print(myuser)

            if(myuser) :

            # Vérification des identifiants
                user = authenticate(username=myuser.username, password =password )
                print('user ', user)
                
                if user is not None:
                        login(request, user)
                        messages.info(request, f"Bienvenue, {myuser.username} !")
                        return redirect('home')  # Redirige vers votre page d'accueil
                else:
                        messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
            else:
                    messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
       
    
                
    return render(request, 'login.html', )
