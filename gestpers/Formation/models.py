from django.db import models
from Userprofile.models import User
# Create your models here.
from django.utils import timezone
from Service.models import  Service
# Définition des énumérations
class CibleChoices(models.TextChoices):
    SERVICE = 'service', 'SERVICE'
    USER = 'user', 'USER'
class TypeChoices(models.TextChoices):
       PRESENTIEL = 'presentiel', 'PRESENTIEL'
       ENLIGNE = 'en_ligne', 'EN LIGNE'
class StatutChoices(models.TextChoices):
        EN_ATTENTE = 'en_attente', 'EN_ATTENTE'
        REJETE = 'rejete', 'REJETE'
        DISPONIBLE = 'disponible', 'DISPONIBLE'
class myStatutChoices(models.TextChoices):
        VALIDE = 'valide', 'VALIDE'
        REJETE = 'rejete', 'REJETE'
class Formation(models.Model):
    titre = models.CharField(max_length=255)
    auteur = models.CharField(max_length=255)
    cible_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    cible_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_concerné")
    cible = models.CharField(
            max_length=10,
            choices=CibleChoices.choices,
            default=CibleChoices.USER
        )
        
    statut = models.CharField(
        max_length=20,
        choices=StatutChoices.choices,
        default=StatutChoices.EN_ATTENTE
    )
    objectifs = models.TextField()
    img_path = models.ImageField(upload_to='formations/') 
    debut = models.DateField(null=True)
    fin = models.DateField(null=True)
    type = models.CharField(
            max_length=10,
            choices=TypeChoices.choices,
            default=TypeChoices.PRESENTIEL
        )
    def __str__(self):
        return self.titre
    @property
    def get_statut(self):
        # On récupère l'heure actuelle avec le fuseau horaire du projet
        now = timezone.now() .date()
        if(self.cible == 'service') :
             return  'disponible' 
        # 1. Si le statut est déjà figé (finalisé), on le retourne
        if self.statut  in [ 'en_attente', 'rejete']:
            return self.statut

        # 2. Logique temporelle (on compare des objets date/datetime)
        if self.fin and self.fin < now:
            return 'termine'
        
        if self.debut and self.debut > now:
            return 'disponible' # (Correction orthographe : disponible)
        
        # 3. Si on est entre début et fin
        return 'en_cours'
                     


class FormationStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    cible = models.CharField(
            max_length=10,
            choices= myStatutChoices.choices,
            default= myStatutChoices.REJETE
        )
    status_date = models.DateField()

    class Meta:
        verbose_name_plural = "Formation statuses"
