from django.db import models
from Userprofile.models import User

class Service(models.Model):
    # Définition des choix
    class TypeChoices(models.TextChoices):
        SERVICE = "service", "SERVICE"
        DIVISION = "division", "DIVISION"
        LABO_PEDAGOGIQUE = "labo_pedagogique", "LABO_PEDAGOGIQUE"
        LABO_RECHERCHE = "labo_recherche", "LABO_RECHERCHE"
        ATELIER = "atelier", "ATELIER"

    class StatutChoices(models.TextChoices):
        ACTIF = 'actif', 'ACTIF'
        NON_ACTIF = 'non_actif', 'NON_ACTIF'

    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sous_services')
    
    # Correction : Utilisation de CharField avec les choix définis
    type = models.CharField(max_length=50, choices=TypeChoices.choices, default=TypeChoices.SERVICE)
    titre = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    statut = models.CharField(max_length=20, choices=StatutChoices.choices, default=StatutChoices.ACTIF)
    
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titre

class ServiceGerant(models.Model):
    # Définition des choix
    class TypeGerantChoices(models.TextChoices):
        EMPLOYE = "employe", "EMPLOYE"
        CHEF = "chef", "CHEF"

    class StatusChoices(models.TextChoices):
        ACTIF = 'actif', 'ACTIF'
        NON_ACTIF = 'non_actif', 'NON_ACTIF'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    
    # Correction : Utilisation de CharField
    type = models.CharField(max_length=20, choices=TypeGerantChoices.choices, default=TypeGerantChoices.EMPLOYE)
    titre = models.CharField(max_length=255)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    update_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.ACTIF)

    def __str__(self):
        return f'{self.user.username}_{self.service.titre}'