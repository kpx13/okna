# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'date')

admin.site.register(Photo, PhotoAdmin)