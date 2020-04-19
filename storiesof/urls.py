"""storiesof URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #expérimentation application Stories
    path('', views.linkedin_homepage, name='linkedin_homepage'),
    path('linkedin_auth_url/', views.linkedin_auth_url, name='linkedin_auth_url'),
    path('linkedin_admin/<profil_linkedin_admin_id>', views.linkedin_admin, name='linkedin_admin'),
    path('linkedin_auth/', views.linkedin_auth, name='linkedin_auth'),
    path('linkedin/<profil_linkedin_admin_id>/<project_id>', views.linkedin, name='linkedin'),
    path('create_project/<profil_linkedin_admin_id>', views.create_project, name='create_project'),
    path('weasyprint_func/', views.weasyprint_func, name='weasyprint_func'),
    path('report/<profil_linkedin_admin_id>/<project_id>', views.report, name='report'),
    path('report_export/<profil_linkedin_admin_id>/<project_id>', views.report_export, name='report_export'),
    path('static/report/',views.staticreport),
    

    path('thanks',views.thanks, name='thanks'),
    path('pay/<profil_linkedin_admin_id>/<project_id>',views.pay, name='pay'),



]
from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)