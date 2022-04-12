from django.db import models
class Item(models.Model):
    name = models.CharField(max_length=254)
    category = models.CharField(max_length=254)
    description = models.TextField()
    brand = models.CharField(max_length=254)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class ItemDiscount(models.Model):
    item = models.ForeignKey('Item', null=True, blank=True, on_delete=models.SET_NULL)
    discount_procent = models.DecimalField(max_digits=6, decimal_places=2)

