from django.contrib import admin
from .models import Personne

# Register your models here.

@admin.register(Personne)
class PersonneAdmin(admin.ModelAdmin):
    pass