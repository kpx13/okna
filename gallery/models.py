# -*- coding: utf-8 -*-
from django.db import models
import pytils

class Photo(models.Model):
    image = models.ImageField(upload_to=lambda instance, filename: 'uploads/gallery/' + pytils.translit.translify(filename),
	max_length=512, verbose_name=u'картинка')
    date = models.DateField(auto_now_add=True, blank=True, verbose_name=u'дата написания')
    
    class Meta:
        verbose_name = u'фотография'
        verbose_name_plural = u'фотографии'
    
    def __unicode__(self):
        return str(self.id)
