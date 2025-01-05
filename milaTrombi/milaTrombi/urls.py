
from django.contrib import admin
from django.urls import path
from App import views

from django.conf import settings
from django.conf.urls.static import static  # new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('affiche/cv/',views.showCv, name='showCv'),
    path('nouvele-personne/',views.ajouterPersonne, name='ajouterPersonne')
]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
