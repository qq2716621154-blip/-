from django.db import models
from symtable import Class
# Create your models here.
class UserInfo(models.Model):
    id = models.CharField(primary_key=True,max_length=32)
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    age = models.IntegerField()

