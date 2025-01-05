from django.shortcuts import render

# Create your views here.
def showCv(request):
    return render(request, 'formatCv/defaut.html')

# enregistrer une nouvelle personne
def ajouterPersonne(request):
    if request.method == "POST":
        pass

    else:
        return render(request, 'cv/ajouterPersonne.html')