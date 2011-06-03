""" Test application 
"""
from django.db import models

# Create your models here.

class BaseClass(models.Model):
    key = models.PositiveIntegerField(unique=True)

class SubClassA(BaseClass):
    class Meta:
            proxy = True

class SubClassB(BaseClass):pass


class SubClassC(BaseClass):
    class Meta:
            proxy = True


class OtherClass(models.Model):
    key = models.PositiveIntegerField(unique=True)

class OtherSubClassA(OtherClass):
    class Meta:
            proxy = True
    
