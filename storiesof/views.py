# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from datetime import datetime


from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import ProfilLinkedin, ProfilLinkedinAdmin

import requests                                 # To use request package in current program 

CLIENT_ID = '789z7ztvzx8pgv'
CLIENT_SECRET = 'y7NUzHM9yimbi2xZ'
REDIRECT_URL = 'https://storiesof.herokuapp.com/linkedin_auth/'

def redirect_view(request,url):
    response = redirect(url)
    return response

def linkedin_auth_url(request):
    

    linkedin_authorization_code_url = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id='+ CLIENT_ID + '&redirect_uri=' + REDIRECT_URL + '&state=' + 'fooobar' + '&scope=r_liteprofile%20r_emailaddress%20w_member_social'    

    response = redirect(linkedin_authorization_code_url)
    return response

def linkedin_homepage(request):
    CLIENT_ID = '789z7ztvzx8pgv'
    CLIENT_SECRET = 'y7NUzHM9yimbi2xZ'
    
    
    linkedin_authorization_code_url = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id='+ CLIENT_ID + '&redirect_uri=' + REDIRECT_URL + '&state=' + 'fooobar' + '&scope=r_liteprofile%20r_emailaddress%20w_member_social'    

    return render(request, 'storiesof/linkedin_homepage.html',{'linkedin_authorization_code_url':linkedin_authorization_code_url})



def linkedin_auth(request):
    
    import urllib.parse as urlparse
    from urllib.parse import parse_qs

    parsed = urlparse.urlparse(str(request))
    authorization_code = parse_qs(parsed.query)['code'][0]

    authorization_state = parse_qs(parsed.query)['state'][0]


    access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&code='+authorization_code +'&redirect_uri=' + REDIRECT_URL + '&client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET
    data_token = requests.get(access_token_url)

    import json

    token = json.loads(str(data_token.text))

    access_token = token['access_token']

    url = 'https://api.linkedin.com/v2/me?oauth2_access_token='+ access_token
    data = requests.get(url)
    data_load = json.loads(str(data.text))


    firstName = data_load['firstName']
    firstName_localized = firstName['localized']
    firstName_fr_FR = firstName_localized['fr_FR']

    lastName = data_load['lastName']
    lastName_localized = lastName['localized']
    lastName_fr_FR = lastName_localized['fr_FR']

    linkedin_id = data_load['id']


    ProfilLinkedinAdmin.objects.filter(linkedin_id=linkedin_id).exists()

    if ProfilLinkedinAdmin.objects.filter(linkedin_id=linkedin_id).exists():
        
        return redirect('../linkedin/'+linkedin_id)
        
    else:
        url2 = 'https://api.linkedin.com/v2/me?projection=(id,profilePicture(displayImage~:playableStreams))&oauth2_access_token='+ access_token
        data2 = requests.get(url2)
        data2_load = json.loads(str(data2.text))
        
        profilePicture = data2_load['profilePicture']
        displayImage = profilePicture['displayImage~']
        elements = displayImage['elements']
        profilepic3 = elements[3]
        identifiers = profilepic3['identifiers']
        identifiers0 = identifiers[0]
        urlpicture = identifiers0['identifier']

        if authorization_state == "fooobar'>":
            profil_linkedin_admin = ProfilLinkedinAdmin()
            profil_linkedin_admin.linkedin_id = linkedin_id
            profil_linkedin_admin.first_name = firstName_fr_FR
            profil_linkedin_admin.last_name = lastName_fr_FR
            profil_linkedin_admin.photo = urlpicture
            profil_linkedin_admin.r_liteprofile = data_load
            profil_linkedin_admin.save()

            return redirect('../linkedin/'+linkedin_id)
        else:
            authorization_state_normal = authorization_state.replace("'>", "")
            print(authorization_state_normal)
            profil_linkedin_admin = ProfilLinkedinAdmin.objects.get(linkedin_id=authorization_state_normal)
            print(profil_linkedin_admin)
            profil_linkedin = ProfilLinkedin()
            profil_linkedin.profil_linkedin_admin_id = profil_linkedin_admin.linkedin_id
            profil_linkedin.linkedin_id = linkedin_id
            profil_linkedin.first_name = firstName_fr_FR
            profil_linkedin.last_name = lastName_fr_FR
            profil_linkedin.photo = urlpicture
            profil_linkedin.r_liteprofile = data_load
            profil_linkedin.save()
            return redirect('../linkedin/'+authorization_state_normal)

    return render(request, 'storiesof/dist/linkedin_auth.html')




def linkedin(request,profil_linkedin_admin_id):
    

    print(profil_linkedin_admin_id)
    profil_linkedin_admin = ProfilLinkedinAdmin.objects.get(linkedin_id=profil_linkedin_admin_id)# Nous sélectionnons tous nos articles
    print(profil_linkedin_admin)

    profils_linkedin = ProfilLinkedin.objects.filter(profil_linkedin_admin_id=profil_linkedin_admin_id)# Nous sélectionnons tous nos articles

    linkedin_authorization_code_url_custom = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=' + CLIENT_ID + '&redirect_uri=' + REDIRECT_URL + '&state=' + profil_linkedin_admin_id + '&scope=r_liteprofile%20r_emailaddress%20w_member_social'
    
    return render(request, 'storiesof/dist/linkedin.html',{'profil_linkedin_admin':profil_linkedin_admin,'profils_linkedin':profils_linkedin,'linkedin_authorization_code_url_custom':linkedin_authorization_code_url_custom})






def view_article(request, id_article):
    """ 
    Vue qui affiche un article selon son identifiant (ou ID, ici un numéro)
    Son ID est le second paramètre de la fonction (pour rappel, le premier
    paramètre est TOUJOURS la requête de l'utilisateur)
    """
    return HttpResponse(
        "Vous avez demandé l'article n° {0} !".format(id_article)    
    )



def lire(request, id):
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'blog/index.html', {'article': article})

def lire_acheteur(request, id):
    try:
        acheteur = Acheteur.objects.get(id=id)
    except Acheteur.DoesNotExist:
        raise Http404

    return render(request, 'blog/index.html', {'acheteur': acheteur})

def lire_revue(request, id):
    try:
        revue = Revue.objects.get(id=id)
    except Revue.DoesNotExist:
        raise Http404

    return render(request, 'blog/index.html', {'revue': revue})




def get_TestForm(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TestForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TestForm()

    return render(request, 'index.html', {'form': form})



def user(request):
    """ Afficher tous les articles de notre blog """
    articles = Article.objects.all() # Nous sélectionnons tous nos articles
    return render(request, 'blog/user.html',{'derniers_articles': articles})




def list_articles(request, month, year):
    """ Liste des articles d'un mois précis. """
    return HttpResponse(
        "Vous avez demandé les articles de {0} {1}.".format(month, year)  
    )








def date_actuelle(request):
    return render(request, 'blog/date.html', {'date': datetime.now()})


def addition(request, nombre1, nombre2):    
    total = nombre1 + nombre2

    # Retourne nombre1, nombre2 et la somme des deux au tpl
    return render(request, 'blog/addition.html', locals())


