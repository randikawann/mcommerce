from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.PositiveBigIntegerField()
    name =  models.CharField(max_length=50)
    cost = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    description = models.TextField()


    def __str__(self):
        return self.name

