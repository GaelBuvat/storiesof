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
    project_related = models.ForeignKey('Project', on_delete=models.CASCADE)
    linkedin_id = models.CharField(blank=True, max_length=100)
    first_name = models.CharField(blank=True, max_length=100)
    last_name = models.CharField(blank=True, max_length=100)
    photo = models.URLField(blank=True)
    photo_report = models.URLField(blank=True)
    photo_static = models.CharField(blank=True, max_length=100)
    r_liteprofile = models.TextField(null=True)
    
    class Meta:
        verbose_name = "ProfilLinkedin"
    
    def __str__(self):
        return self.last_name

class Project(models.Model):
    #penser à rajouter l'id pour sauvegarder l'ID du recruteur ou de l'intéressé
    project_name = models.CharField(blank=True, max_length=100)
    linkedin_admin_id = models.ForeignKey('ProfilLinkedinAdmin', on_delete=models.CASCADE)
    photo_url = models.CharField(blank=True, max_length=100)

    class Meta:
        verbose_name = "Project"
    
    def __str__(self):
        return self.project_name


class OpenFiles():
    def __init__(self):
        self.files = []
    def open(self, file_name):
        f = open(file_name)
        self.files.append(f)
        return f
    def close(self):
        list(map(lambda f: f.close(), self.files))



