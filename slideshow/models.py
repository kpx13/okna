# -*- coding: utf-8 -*-
from django.db import models
from dashboard import string_with_title
import pytils

class Slider(models.Model):
    image = models.ImageField(upload_to=lambda instance, filename: 'uploads/slider/' + pytils.translit.translify(filename),
        max_length=256, verbose_name=u'картинка')
    title = models.CharField(max_length=500, blank=True, verbose_name=u'заголовок')
    text = models.TextField(blank=True, verbose_name=u'текст')
    link = models.CharField(max_length=200, blank=True, verbose_name=u'ссылка')
    order = models.IntegerField(blank=True, null=True, verbose_name=u'порядок сортировки', help_text=u'№ слайдера: 1й, 2й .. 5й')
    
    class Meta:
        verbose_name = 'слайдер'
        verbose_name_plural = 'слайдер'
        app_label = string_with_title("slideshow", u"Слайдшоу")
        ordering = ['order']
        
    
    def __unicode__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        super(Slider, self).save(*args, **kwargs)
        if not self.order:
            self.order = self.id
            self.save()