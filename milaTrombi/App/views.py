from django.shortcuts import render, redirect, get_object_or_404
from .models import Personne, Cv, Loisir, Competence, ExperienceProfessionnelle, Formation
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

        # Vérifier si tous les champs obligatoires sont remplis
        if not all([nom, prenoms, telephone, email, adresse, mdp, cmdp]):
            messages.error(request, "Tous les champs doivent être remplis.")
            return redirect('ajouterPersonne')

        # Vérifier si les deux mots de passe sont identiques
        if mdp != cmdp:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('ajouterPersonne')

        # Enregistrer la personne
        try:
            personne = Personne.objects.create_user(
                nom=nom,
                prenom=prenoms,
                telephone=telephone,
                adresse=adresse,
                email=email,
                photo=photo,
            )
            # Définir et sécuriser le mot de passe
            personne.set_password(mdp)
            personne.save()

            # Connecter automatiquement l'utilisateur
            login(request, personne)

            # Redirection après création
            return redirect('description', personne_id=personne.id)
        except Exception as e:
            messages.error(request, f"Une erreur s'est produite : {str(e)}")
            return redirect('ajouterPersonne')

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
        return redirect('formation')

    else:
        user_id = request.session.get("user")
        if not user_id:
            redirect("ajouterPersonne")
        return render(request, 'cv/description.html')
    

def formation(request):
    # Reccuperer l'id du cv gardé en session
    cv = request.session.get("cv_id")
    user_id = request.session.get("user")

    if request.method == "POST":
        etablissement = request.POST.getlist('etablissement')
        diplome = request.POST.getlist('diplome')
        periode = request.POST.getlist('periode')

        cv = get_object_or_404(Cv, id=cv)
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
        if not user_id:
            return redirect('ajouterPersonne')
        if not cv:
            return redirect('description', personnde_id=user_id)
        return render(request, 'cv/formation.html')
    

def experienceProfessionnelle(request):
    # Reccuperer l'id du cv gardé en session
    cv = request.session.get("cv_id")
    user_id = request.session.get("user")

    if request.method == "POST":
        periode = request.POST.getlist('periode')
        poste = request.POST.getlist('poste')
        entreprise = request.POST.getlist('entreprise')
        localite = request.POST.getlist('localite')
        description = request.POST.getlist('description')
        
        cv = get_object_or_404(Cv, id=cv)

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
        if not user_id:
            return redirect('ajouterPersonne')
        if not cv:
            return redirect('description', personnde_id=user_id)
        
        return render(request, 'cv/experience_pro.html')
    

def competence(request):
    # Reccuperer l'id du cv gardé en session
    cv = request.session.get("cv_id")
    user_id = request.session.get("user")
    
    if request.method == "POST":
        competence = request.POST.getlist('competence')
        niveau = request.POST.getlist('niveau')

        cv = get_object_or_404(Cv, id=cv)
        # enregistrer le ou les formation(s)
        for i in range(len(niveau)):
            Competence.objects.create(
                competence=competence[i],
                niveau=niveau[i],
                cv=cv
            )
        return redirect('experience_pro')
    else:
        if not user_id:
            return redirect('ajouterPersonne')
        if not cv:
            return redirect('description', personnde_id=user_id)
        return render(request, 'cv/competence.html')
    

def langue(request):
    # Reccuperer l'id du cv gardé en session
    cv = request.session.get("cv_id")
    user_id = request.session.get("user")

    if request.method == "POST":
        langue = request.POST.getlist('langue')
        niveau = request.POST.getlist('niveau')
        
        cv = get_object_or_404(Cv, id=cv)

        # enregistrer le ou les formation(s)
        for i in range(len(niveau)):
            Competence.objects.create(
                langue=langue[i],
                niveau=niveau[i],
                cv=cv
            )
        return redirect('loisirs')
    else:
        if not user_id:
            return redirect('ajouterPersonne')
        if not cv:
            return redirect('description', personnde_id=user_id)
        return render(request, 'cv/langue.html')
    

def loisirs(request):
    cv = request.session.get("cv_id")
    user_id = request.session.get("user")
    if request.method == "POST":
        loisirs = request.POST.getlist('loisirs')

        cv = get_object_or_404(Cv, id=cv)
        # enregistrer le ou les formation(s)
        for i in range(len(loisirs)):
            Loisir.objects.create(
                loisirs=loisirs[i],
                cv=cv
        )
        del request.session['cv_id']
        del request.session['user']
        request.session["slug"] = True
        return redirect('connexion')
    
    else:
        if not user_id:
            return redirect('ajouterPersonne')
        if not cv:
            return redirect('description', personnde_id=user_id)
        return render(request, 'cv/loisirs.html')
    
# gerer la connexion de l'utilisateur
def connexion(request):
    context = {}
    if request.method == "POST":
        if request.session.get('slug'):
            del request.session['slug']

        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(email=email, password=password)
        
        if user:
            login(request, user)
            # request.session["user"] = user
            return redirect('profil')
        else:
            context['error'] = True
            return render(request, "utilisateur/connexion.html", context)
    else:
        slug = request.session.get("slug")
        if slug:
            context["slug"] = slug

        return render(request, "utilisateur/connexion.html", context)

def deconnexion(request):
    logout(request)
    return redirect("connexion")

@login_required
def profil(request):
    return render(request, "utilisateur/profil/home.html")

@login_required
def selectTemplate(request):
    return render(request, "utilisateur/profil/templateCv/index.html")



def format(request):
    return render(request, "formatCv/defaut.html")