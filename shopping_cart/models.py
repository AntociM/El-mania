from django.db import models
from store.models import Item
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.

class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    user_id = models.IntegerField()
    total = models.DecimalField(max_digits=6, decimal_places=2)
    created_at  = models.DateTimeField()
    modified_at = models.DateTimeField()