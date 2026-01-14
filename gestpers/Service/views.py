from django.shortcuts import render,get_object_or_404 ,redirect 
from .models import *
from django.views.generic import DeleteView
# Create your views here.

from django.urls import reverse_lazy

def service_create(request):
    if request.method == "POST":
        # Extraction des données selon votre structure HTML
        titre = request.POST.get('titre')  # correspond à name="titre"
        code = request.POST.get('code')
        service_type = request.POST.get('type')
        parent_id = request.POST.get('parent')
        statut = request.POST.get('status')
        # Si vous avez ajouté un champ description dans le modèle :
        # description = request.POST.get('description')

        parent = None
        if parent_id:
            parent = get_object_or_404(Service, id=parent_id)

        # Création de l'objet
        Service.objects.create(
            titre=titre,
            code=code,
            type=service_type,
            parent=parent,
            statut=statut
        )
        # Redirection vers la liste après succès
        return redirect('dashbord_admin')
    
    # Si GET, on affiche le formulaire (avec les parents possibles pour le select)
    parents = Service.objects.all()
    return render(request, 'admin/AjouterService.html', {'parents': parents , })


def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == "POST":
        service.titre = request.POST.get('titre')
        service.code = request.POST.get('code')
        service.type = request.POST.get('type')
        service.statut = request.POST.get('status')
        
        parent_id = request.POST.get('parent')
        if parent_id:
            service.parent = get_object_or_404(Service, id=parent_id)
        else:
            service.parent = None
            
        service.save()
        return redirect('dashbord_admin')

    parents = Service.objects.exclude(pk=pk) # On ne peut pas être son propre parent
    return render(request, 'admin/AjouterService.html', {
        'service': service, 
        'parents': parents,
        'is_edit': True
    })


def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == "POST":
            service.delete()
            return redirect('dashbord_admin')

    return render(request, 'admin/delete.html',{'objet' : service} )

