from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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
    discount_procent = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    new_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def update_new_price(self):
        if self.new_price != round(self.item.price - (self.discount_procent * self.item.price) / 100, 2):
            self.new_price = round(self.item.price - (self.discount_procent * self.item.price) / 100, 2)
            self.save()
