from django.shortcuts import render, redirect, get_object_or_404
from .models import Personne, Cv, Loisir, Competence, ExperienceProfessionnelle, Formation
from django.contrib.auth import authenticate, login

# Create your views here.
def showCv(request):
    return render(request, 'formatCv/defaut.html')

# enregistrer une nouvelle personne
def ajouterPersonne(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        prenoms = request.POST.get('prenoms')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        mdp = request.POST.get('mdp')
        cmdp = request.POST.get('cmdp')
        photo = request.FILES.get('photo')

        # verifier si les deux mots de passe sont identique
        if mdp != cmdp:
            return redirect('ajouterPersonne')
        
        # Enregistrer la personne 
        personne = Personne.objects.create_user(
            nom=nom,
            prenom=prenoms,
            telephone=telephone,
            adresse=adresse,
            email=email,
            photo=photo
        )
        return redirect('description', personnde_id=personne.id)

    else:
        return render(request, 'cv/ajouterPersonne.html')
    

def description(request, personnde_id):
    if request.method == "POST":
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        personne = get_object_or_404(Personne, id=personnde_id)

        cv = Cv.objects.create(
            poste=titre,
            description=description,
            personne=personne
        )

        # Garder l'id du cv en session 
        request.session["cv_id"] = cv.id

    else:
        return render(request, 'cv/description.html')
    

def formation(request):
    if request.method == "POST":
        etablissement = request.POST.getlist('etablissement')
        diplome = request.POST.getlist('diplome')
        periode = request.POST.getlist('periode')
        
        # Reccuperer l'id du cv gardé en session
        cv = get_object_or_404(Cv, id=request.session.get('cv_id'))

        # enregistrer le ou les formation(s)
        for i in range(len(diplome)):
            Formation.objects.create(
                etablissement=etablissement[i],
                diplome=diplome[i],
                periode=periode[i],
                cv=cv
            )
        return redirect('competence')
    else:
        return render(request, 'cv/formation.html')
    

def experienceProfessionnelle(request):
    if request.method == "POST":
        periode = request.POST.getlist('periode')
        poste = request.POST.getlist('poste')
        entreprise = request.POST.getlist('entreprise')
        localite = request.POST.getlist('localite')
        description = request.POST.getlist('description')
        
        # Reccuperer l'id du cv gardé en session
        cv = get_object_or_404(Cv, id=request.session.get('cv_id'))

        # enregistrer le ou les formation(s)
        for i in range(len(periode)):
            ExperienceProfessionnelle.objects.create(
                job_titre=poste[i],
                entreprise=entreprise[i],
                localite=localite[i],
                periode=periode[i],
                description=description[i],
                cv=cv
            )
        return redirect('langue')
    else:
        return render(request, 'cv/experience_pro.html')
    

def competence(request):
    if request.method == "POST":
        competence = request.POST.getlist('competence')
        niveau = request.POST.getlist('niveau')
        
        # Reccuperer l'id du cv gardé en session
        cv = get_object_or_404(Cv, id=request.session.get('cv_id'))

        # enregistrer le ou les formation(s)
        for i in range(len(niveau)):
            Competence.objects.create(
                competence=competence[i],
                niveau=niveau[i],
                cv=cv
            )
        return redirect('experience_pro')
    else:
        return render(request, 'cv/competence.html')
    

def langue(request):
    if request.method == "POST":
        langue = request.POST.getlist('langue')
        niveau = request.POST.getlist('niveau')
        
        # Reccuperer l'id du cv gardé en session
        cv = get_object_or_404(Cv, id=request.session.get('cv_id'))

        # enregistrer le ou les formation(s)
        for i in range(len(niveau)):
            Competence.objects.create(
                langue=langue[i],
                niveau=niveau[i],
                cv=cv
            )
        return redirect('loisirs')
    else:
        return render(request, 'cv/langue.html')
    

def loisirs(request):
    if request.method == "POST":
        loisirs = request.POST.getlist('loisirs')
        
        # Reccuperer l'id du cv gardé en session
        cv = get_object_or_404(Cv, id=request.session.get('cv_id'))

        # enregistrer le ou les formation(s)
        for i in range(len(loisirs)):
            Loisir.objects.create(
                loisirs=loisirs[i],
                cv=cv
        )
        del request.session['cv_id']
        request.session["slug"] = True
        return redirect('connexion')
    else:
        return render(request, 'cv/loisirs.html')
    
# gerer la connexion de l'utilisateur
def connexion(request):
    context = {}
    if request.method == "POST":
        email = request.POST.getlist('email')
        password = request.POST.getlist('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            # request.session["user"] = user
            # return redirect('profil')
        else:
            context['error'] = True
            return render(request, "utilisateur/connexion.html", context)
    else:
        slug = request.session.get("slug")
        if slug:
            context["slug"] = slug

        return render(request, "utilisateur/connexion.html", context)
    
def profil(request):
    pass