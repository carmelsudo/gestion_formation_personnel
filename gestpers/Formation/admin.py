from django.contrib import admin
from Service.models import *
from Userprofile.models import *
from Formation.models import *
# Register your models here.
admin.site.register(Formation)
admin.site.register(FormationStatus)
admin.site.register(Service)
admin.site.register(User)
admin.site.register(ServiceGerant)