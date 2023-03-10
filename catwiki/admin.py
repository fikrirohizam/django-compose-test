from django.contrib import admin

# Register your models here.
from .models import Home,Human,Breed,Cat

admin.site.register(Home)
admin.site.register(Human)
admin.site.register(Breed)
admin.site.register(Cat)
