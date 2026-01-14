from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import  LogoutView
from .form import *
# Create your views here.
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from Service.models import *
from Formation.models import *
from .models import User
def home(request) :
    return render(request , 'home.html')


def Subordonne(request) :
    
    return render(request , 'subordonne.html')

# views.py


def register(request):
    form = inscriptionForm()
    if request.method == 'POST':
        form = inscriptionForm(request.POST)
        if(form.is_valid()):
            service = form.cleaned_data['services']
            user = None
            try:
                user = form.save()
                ServiceGerant.objects.create(service = service , user = user ,titre = service.titre )
                messages.success(request, f"Compte Creeé, ")
                return redirect('login')
            except Exception as e :
                if user : 
                      user.delete()
                messages.error(request, f"{e}")


        else:
                    messages.error(request, f"Remplissez corectement le formulaire ")
       
    
                
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


from django.contrib.auth.hashers import make_password

def personnel_create_view(request):
    # Récupération des groupes pour le menu déroulant

    if request.method == 'POST':
        # 1. Récupération des données brutes
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('passwordConfirm')
        group = request.POST.get('group')
        avatar = request.FILES.get('avatar')

        # 2. Validation manuelle
        errors = {}
        if not last_name or len(last_name) < 2:
            errors['lastName'] = "Le nom est requis."
        
        if User.objects.filter(email=email).exists():
            errors['email'] = "Cet email est déjà utilisé."
            
        if password != password_confirm:
            errors['passwordMatch'] = "Les mots de passe ne correspondent pas."

        # 3. Traitement si valide
        if not errors:
            try:
         
                user = User.objects.create(
                    last_name=last_name,
                    email=email,
                    username=email, # Django User requiert un username unique
                    password=make_password(password),
                    group = group,
                    avatar = avatar
                )

               

                # Gestion de l'avatar (Si vous avez un profil lié)
                # if avatar:
                #     user.profile.avatar = avatar
                #     user.profile.save()

                messages.success(request, "Personnel ajouté avec succès !")
                return redirect('liste_personnel') # Changez vers votre URL de redirection

            except Exception as e:
                errors['server'] = f"Une erreur est survenue : {e}"
        
        # Si erreurs, on renvoie la page avec les erreurs et les données saisies
        return render(request, 'votre_template.html', {
            'errors': errors,
            'data': request.POST
        })

    return render(request, 'votre_template.html', )

def dashbord_admin(request) : 
     formations = Formation.objects.all().order_by('-id')
     services = Service.objects.all().order_by('-id')
     serviceGerants = ServiceGerant.objects.all().order_by('-id')

     return render(request, "admin/dashboard_admin.html" , {
          "formations": formations,  
          'services':services,
          'serviceGerants':serviceGerants,
     })

def subordonné_view(request, pk):
    """
    Vue pour afficher les formations et détails d'un utilisateur spécifique.
    Récupère les données d'un seul utilisateur par son ID (pk).
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        messages.error(request, "Utilisateur non trouvé.")
        return redirect('home')
    
    # Récupérer les formations de cet utilisateur
    formations = Formation.objects.filter(cible_user=user).order_by('-id')
    
    # Récupérer le ServiceGerant de cet utilisateur
    service_gerant = ServiceGerant.objects.filter(user=user).first()
    
    # Calculer les statistiques
    formations_in_progress = formations.filter(statut='en_cours').count()
    formations_completed = formations.filter(statut='terminé').count()
    formations_validated = Formation.objects.filter(
        cible_user=user,
        statut = "valide"
    ).count()
    
    context = {
        'user': user,
        'service_gerant': service_gerant,
        'formations': formations,
        'formations_count': formations.count(),
        'formations_in_progress': formations_in_progress,
        'formations_completed': formations_completed,
        'formations_validated': formations_validated,
    }
    
    return render(request, 'surbordonnéView.html', context) 
   
def Logout(request) :
    logout(request)
    return redirect('inscription')
