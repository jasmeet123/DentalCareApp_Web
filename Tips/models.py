from __future__ import unicode_literals

from django.db import models
from datetime import date
from django.contrib import admin
from django.contrib.auth.models import User
from dentist_login.models import Dentist
from DentalCare import settings
import os


class Tip(models.Model):
    id = models.AutoField(primary_key=True);
    title = models.CharField(max_length= 200);
    desc = models.CharField(max_length=1000);
    image = models.ImageField(upload_to="tips_image/",default=os.path.join(settings.MEDIA_ROOT,settings.MEDIA_URL,'tips_image/Holiday_Party_Img4.jpg'))
    date = models.DateField(default=date.today())
    owner = models.ForeignKey(Dentist, related_name='tips')

    # owner = models.ForeignKey('User', blank=True, null=True, related_name='tips')

    def __str__(self):
        return self.title

    def save(self, *args,**kwargs):
        super(Tip,self).save(*args,**kwargs)
