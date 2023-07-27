from django.db import models
from django.contrib.auth.models import User

# Create your models here.





class Bank(models.Model):
    """ """
    name = models.CharField(max_length=200)
    swift_code = models.CharField(max_length=200)
    inst_num = models.CharField(max_length=200, verbose_name='Institution Number')
    description = models.CharField(max_length=200, blank=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                              blank=True)



    def __str__(self):

        return f"{self.name}"
    