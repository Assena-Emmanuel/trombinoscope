from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Personne(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    last_name = None
    first_name = None

    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    telephone = models.CharField(max_length=30)
    adresse = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="photos/")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'telephone',]

class Cv(models.Model):
    poste = models.CharField(max_length=225)
    description = models.TextField()
    photo = models.ImageField(upload_to="cvPhoto/", null=True)
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE)

class Formation(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    etablissement = models.CharField(max_length=255)
    diplome = models.CharField(max_length=255)
    periode = models.CharField(max_length=4)

class Loisir(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    loisirs = models.CharField(max_length=255)

class ExperienceProfessionnelle(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    job_titre = models.CharField(max_length=255)
    entreprise = models.CharField(max_length=255)
    localite = models.CharField(max_length=255, null=True)
    periode = models.CharField(max_length=50)
    description = models.TextField()

class Langue(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    language = models.CharField(max_length=100)
    niveau = models.CharField(max_length=50)

class Competence(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    competence = models.CharField(max_length=255)
    niveau = models.CharField(max_length=50)
