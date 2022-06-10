import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField
from store.models import Item

from model_utils.fields import StatusField
from model_utils import Choices
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class Order(models.Model):
    order_number = models.CharField(
        max_length=40, null=False, editable=False, primary_key=True)
    user_id = models.IntegerField(null=True)
    payment_id = models.IntegerField(null=True)
    full_name = models.CharField(max_length=254, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = PhoneNumberField(null=False, blank=False, unique=False)
    country = CountryField(null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    delivery_cost = models.DecimalField(
        max_digits=4, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    notes = models.TextField(null=True, blank=True)

    STATUS = Choices('processing', 'delivered')

    status = StatusField(null=False)

    def generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        # self.save()
        pass

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, null=False, on_delete=models.CASCADE, related_name='orderitems')
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    order_item_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=False, editable=False)
