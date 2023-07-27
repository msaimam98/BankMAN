from django.db import models
from banks.models.banks import Bank



class Branch(models.Model):
    """ """
    name = models.CharField(max_length=200)
    transit_num = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    email = models.EmailField(default='admin@utoronto.ca')

    # this is a non-negative integar 
    capacity = models.PositiveBigIntegerField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    bank = models.ForeignKey(Bank, null=True, on_delete=models.CASCADE,
                              blank=True, related_name='branches')


    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = 'branches'
