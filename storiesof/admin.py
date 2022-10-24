# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.text import Truncator


# Register your models here.
from .models import ProfilLinkedin, ProfilLinkedinAdmin, Project



admin.site.register(ProfilLinkedinAdmin)
admin.site.register(Project)
admin.site.register(ProfilLinkedin)



