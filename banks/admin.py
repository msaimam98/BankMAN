from django.contrib import admin
from banks.models.banks import Bank
from banks.models.branches import Branch


# Register your models here.


admin.site.register(Bank) 
admin.site.register(Branch)