"""
URL configuration for gestpers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from .views import *  

urlpatterns = [
    
   path('' , get_all_formations , name='formations' ),
   path('demandes' , get_all_demandes , name='demandes' ),
   path('demandes/create' , create_demande , name='create_demande' ),
   path('demandes/details/<int:id>' , get_one_formations , name='formation_details' ),
   path('demandes/valider/<int:pk>' , valider , name='formation_valider' ),
   path('demandes/rejeter/<int:pk>' , rejeter , name='formation_rejeter' ),
   path('demandes/create/new/<int:pk>' , nouvel_version_demande , name='nouvel_version_demande' ),
  
    path('admin/formations/nouveau/', FormationCreateView.as_view(), name='formation_create'),
    path('admin/formations/<int:pk>/modifier/', FormationUpdateView.as_view(), name='formation_update'),
    path('admin/formations/<int:pk>/supprimer/', FormationDeleteView.as_view(), name='formation_delete'),
   

]
