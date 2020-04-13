# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Create your models here.
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from django.db import models



class ProfilLinkedinAdmin(models.Model):
    #penser à rajouter l'id pour sauvegarder l'ID du recruteur ou de l'intéressé
    linkedin_id = models.CharField(blank=True, max_length=100)
    first_name = models.CharField(blank=True, max_length=100)
    last_name = models.CharField(blank=True, max_length=100)
    photo = models.URLField(blank=True)
    r_liteprofile = models.TextField(null=True)
    
    class Meta:
        verbose_name = "ProfilLinkedinAdmin"
    
    def __str__(self):
        return self.last_name

class ProfilLinkedin(models.Model):
    #penser à rajouter l'id pour sauvegarder l'ID du recruteur ou de l'intéressé
    profil_linkedin_admin_id = models.CharField(blank=True, max_length=100)
    linkedin_id = models.CharField(blank=True, max_length=100)
    first_name = models.CharField(blank=True, max_length=100)
    last_name = models.CharField(blank=True, max_length=100)
    photo = models.URLField(blank=True)
    r_liteprofile = models.TextField(null=True)
    
    class Meta:
        verbose_name = "ProfilLinkedin"
    
    def __str__(self):
        return self.last_name


