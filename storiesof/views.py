# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from datetime import datetime


from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from .models import ProfilLinkedin, ProfilLinkedinAdmin, Project

import requests                                 # To use request package in current program 

CLIENT_ID = '789z7ztvzx8pgv'
CLIENT_SECRET = 'y7NUzHM9yimbi2xZ'
#  http://127.0.0.1:8001/ https://storiesof.herokuapp.com/
URL_RACINE = 'https://storiesof.herokuapp.com/'
REDIRECT_URL = URL_RACINE+'linkedin_auth/'

linkedin_authorization_code_url = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id='+ CLIENT_ID + '&redirect_uri=' + REDIRECT_URL + '&state=' + 'fooobar' + '&scope=r_liteprofile%20r_emailaddress%20w_member_social'    


def redirect_view(request,url):
    response = redirect(url)
    return response

def linkedin_auth_url(request):
    
    response = redirect(linkedin_authorization_code_url)
    return response

def weasyprint_func(request):
    import weasyprint
    from weasyprint import HTML, CSS
    r = requests.get(request)
    print(r.text)
    pdf = weasyprint.HTML(r.text).write_pdf('google.pdf', )
    
    response = redirect(URL_RACINE+'linkedin/fI5gp_jpKM/23')
    return response

def report(request,profil_linkedin_admin_id,project_id):

    profil_linkedin_admin = ProfilLinkedinAdmin.objects.get(linkedin_id=profil_linkedin_admin_id)# Nous sélectionnons le profil admin related

    profils_linkedin = ProfilLinkedin.objects.filter(project_related=project_id)# Nous sélectionnons tous nos articles

    return render(request, 'storiesof/report.html',{'profil_linkedin_admin':profil_linkedin_admin,'profils_linkedin':profils_linkedin,'profil_linkedin_admin_id':profil_linkedin_admin_id})


def report_export(request,profil_linkedin_admin_id,project_id):
    profil_linkedin_admin = ProfilLinkedinAdmin.objects.get(linkedin_id=profil_linkedin_admin_id)# Nous sélectionnons le profil admin related

    profils_linkedin = ProfilLinkedin.objects.filter(project_related=project_id)# Nous sélectionnons tous nos articles

    import weasyprint
    from weasyprint import HTML, CSS
    report_url = URL_RACINE + 'report/' + profil_linkedin_admin_id + '/' + project_id

    nb_profils = len(profils_linkedin)
    i=0
    while i < nb_profils:
        profil_linkedin = profils_linkedin[i]
        profil_linkedin_url = profil_linkedin.photo_report
        fileName = 'static/assets/img/profiles/profile_'+profil_linkedin.first_name+'.png'
        req = requests.get(profil_linkedin_url)
        file = open(fileName, 'wb')
        profil_linkedin.photo_static = '../../'+file.name
        profil_linkedin.save()
        for chunk in req.iter_content(100000):
            file.write(chunk)
        file.close()
        i=i+1
    

    profils_linkedin = ProfilLinkedin.objects.filter(project_related=project_id)# Nous sélectionnons tous nos articles
    
    r = requests.get(report_url)
    fichier_html = open("static/html/data.html", "w")
    fichier_html.write(str(r.text))
    fichier_html.close()
    pdf = weasyprint.HTML(fichier_html.name).write_pdf('static/report/report.pdf', )

    i=1
    if i==1:
        response = redirect(URL_RACINE+ 'linkedin/' + profil_linkedin_admin_id + '/' + project_id)    
        return response
    

    return render(request, 'storiesof/report.html',{'profil_linkedin_admin':profil_linkedin_admin,'profils_linkedin':profils_linkedin,'linkedin_authorization_code_url_custom':linkedin_authorization_code_url_custom,'profil_linkedin_admin_id':profil_linkedin_admin_id})




def linkedin_homepage(request):
    
    return render(request, 'storiesof/linkedin_homepage.html',{'linkedin_authorization_code_url':linkedin_authorization_code_url})

def linkedin_admin(request,profil_linkedin_admin_id):
    projects = Project.objects.filter(linkedin_admin_id__linkedin_id=profil_linkedin_admin_id)# Nous sélectionnons tous nos articles
    profil_admin = ProfilLinkedinAdmin.objects.get(linkedin_id=profil_linkedin_admin_id)

    return render(request, 'storiesof/linkedin_admin.html',{'projects':projects, 'profil_linkedin_admin_id':profil_linkedin_admin_id,'profil_admin':profil_admin})

def create_project(request,profil_linkedin_admin_id):
    profil_admin = ProfilLinkedinAdmin.objects.get(linkedin_id=profil_linkedin_admin_id)

    project = Project()
    project.name = 'test'
    project.linkedin_admin_id = profil_admin
    project.photo_url = 'https://source.unsplash.com/n3sqjJzZiBM/400x300'
    project.save()

    projects = Project.objects.filter(linkedin_admin_id__linkedin_id=profil_linkedin_admin_id)
    project_id = str(projects[len(projects)-1].id)
    return redirect('../linkedin/'+profil_linkedin_admin_id+'/'+project_id)



def linkedin_auth(request):
    
    import urllib.parse as urlparse
    from urllib.parse import parse_qs

    parsed = urlparse.urlparse(str(request))
    authorization_code = parse_qs(parsed.query)['code'][0]

    authorization_state = parse_qs(parsed.query)['state'][0]


    # Phase de demande d'informations concernant la personne qui se connecte
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

    url2 = 'https://api.linkedin.com/v2/me?projection=(id,profilePicture(displayImage~:playableStreams))&oauth2_access_token='+ access_token
    data2 = requests.get(url2)
    data2_load = json.loads(str(data2.text))
        
    profilePicture = data2_load['profilePicture']
    displayImage = profilePicture['displayImage~']
    elements = displayImage['elements']
    profilepic3 = elements[3]
    identifiers3 = profilepic3['identifiers']
    identifiers3_0 = identifiers3[0]
    urlpicture3 = identifiers3_0['identifier']

    profilepic1 = elements[1]
    identifiers1 = profilepic1['identifiers']
    identifiers1_0 = identifiers1[0]
    urlpicture1 = identifiers1_0['identifier']


    profil_admin_verif = ProfilLinkedinAdmin.objects.filter(linkedin_id=linkedin_id).exists()
    profil_verif = ProfilLinkedin.objects.filter(linkedin_id=linkedin_id).exists()

    if profil_admin_verif:
        
        if authorization_state == "fooobar'>":
            return redirect('../linkedin_admin/'+linkedin_id)
        else:
            authorization_state_normal = authorization_state.replace("'>", "")

            project = Project.objects.get(id=authorization_state_normal)
            
            # project.photo_url = urlpicture project.save()

            profil_linkedin_admin_id = project.linkedin_admin_id.linkedin_id

            profil_linkedin_verif= ProfilLinkedin.objects.filter(project_related=project).filter(linkedin_id=linkedin_id).exists()

            if profil_linkedin_verif:
                return redirect('../linkedin/'+profil_linkedin_admin_id+'/'+authorization_state_normal)
            else:
                
                profil_linkedin = ProfilLinkedin()
                profil_linkedin.project_related = project
                profil_linkedin.linkedin_id = linkedin_id
                profil_linkedin.first_name = firstName_fr_FR
                profil_linkedin.last_name = lastName_fr_FR
                profil_linkedin.photo = urlpicture3
                profil_linkedin.photo_report = urlpicture1
                profil_linkedin.r_liteprofile = data_load
                profil_linkedin.save()
                return redirect('../linkedin/'+profil_linkedin_admin_id+'/'+authorization_state_normal)
    elif profil_verif:


        if authorization_state == "fooobar'>":
            profil_linkedin_admin = ProfilLinkedinAdmin()
            profil_linkedin_admin.linkedin_id = linkedin_id
            profil_linkedin_admin.first_name = firstName_fr_FR
            profil_linkedin_admin.last_name = lastName_fr_FR
            profil_linkedin_admin.photo = urlpicture3
            profil_linkedin.photo_report = urlpicture1
            profil_linkedin_admin.r_liteprofile = data_load
            profil_linkedin_admin.save()
            return redirect('../linkedin_admin/'+linkedin_id)
        else:
            authorization_state_normal = authorization_state.replace("'>", "")

            project = Project.objects.get(id=authorization_state_normal)
            
            # project.photo_url = urlpicture project.save()


            profil_linkedin_admin_id = project.linkedin_admin_id.linkedin_id

            profil_linkedin_verif= ProfilLinkedin.objects.filter(project_related=project).filter(linkedin_id=linkedin_id).exists()

            if profil_linkedin_verif:
                return redirect('../linkedin/'+profil_linkedin_admin_id+'/'+authorization_state_normal)
            else:
                profil_linkedin = ProfilLinkedin()
                profil_linkedin.project_related = project
                profil_linkedin.linkedin_id = linkedin_id
                profil_linkedin.first_name = firstName_fr_FR
                profil_linkedin.last_name = lastName_fr_FR
                profil_linkedin.photo = urlpicture3
                profil_linkedin.photo_report = urlpicture1
                profil_linkedin.r_liteprofile = data_load
                profil_linkedin.save()
                return redirect('../linkedin/'+profil_linkedin_admin_id+'/'+authorization_state_normal)
    else:
        if authorization_state == "fooobar'>":
            profil_linkedin_admin = ProfilLinkedinAdmin()
            profil_linkedin_admin.linkedin_id = linkedin_id
            profil_linkedin_admin.first_name = firstName_fr_FR
            profil_linkedin_admin.last_name = lastName_fr_FR
            profil_linkedin_admin.photo = urlpicture3
            profil_linkedin.photo_report = urlpicture1
            profil_linkedin_admin.r_liteprofile = data_load
            profil_linkedin_admin.save()
            return redirect('../linkedin_admin/'+linkedin_id)
        else:
            authorization_state_normal = authorization_state.replace("'>", "")

            project = Project.objects.get(id=authorization_state_normal)
            
            # project.photo_url = urlpicture project.save()


            profil_linkedin_admin_id = project.linkedin_admin_id.linkedin_id

            profil_linkedin = ProfilLinkedin()
            profil_linkedin.project_related = project
            profil_linkedin.linkedin_id = linkedin_id
            profil_linkedin.first_name = firstName_fr_FR
            profil_linkedin.last_name = lastName_fr_FR
            profil_linkedin.photo = urlpicture3
            profil_linkedin.photo_report = urlpicture1
            profil_linkedin.r_liteprofile = data_load
            profil_linkedin.save()
            return redirect('../linkedin/'+profil_linkedin_admin_id+'/'+authorization_state_normal)

    return render(request, 'storiesof/linkedin_auth.html')




def linkedin(request,profil_linkedin_admin_id,project_id):
    
    profil_linkedin_admin = ProfilLinkedinAdmin.objects.get(linkedin_id=profil_linkedin_admin_id)# Nous sélectionnons le profil admin related

    profils_linkedin = ProfilLinkedin.objects.filter(project_related=project_id)# Nous sélectionnons tous nos articles
    state_custom = project_id

    linkedin_authorization_code_url_custom = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=' + CLIENT_ID + '&redirect_uri=' + REDIRECT_URL + '&state=' + state_custom + '&scope=r_liteprofile%20r_emailaddress%20w_member_social'
    
    return render(request, 'storiesof/linkedin.html',{'profil_linkedin_admin':profil_linkedin_admin,'profils_linkedin':profils_linkedin,'linkedin_authorization_code_url_custom':linkedin_authorization_code_url_custom,'profil_linkedin_admin_id':profil_linkedin_admin_id,'project_id':project_id})




