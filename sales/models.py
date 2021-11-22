from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from .utils import generate_code

# Create your models here.

class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(blank=True)
    created = models.DateTimeField(blank=True)  # so that it's possible to edit this in admin panel

    def __str__(self):
        return f"Sold {self.quantity} units of {self.product.name} for ${self.price}."

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        return super().save(*args, **kwargs)

    def get_sale_id(self):
        return self.sale_set.first().sale_id

class Sale(models.Model):
    sale_id = models.CharField(max_length=12, blank=True)
    positions = models.ManyToManyField(Position)
    total_price = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sales of ${self.total_price}"

    def save(self, *args, **kwargs):
        if self.sale_id == '':
            self.sale_id = generate_code()
        if self.created is None:
            self.created = timezone.now()
        # self.total_price = sum([p.price for p in self.get_positions()])
        return super().save(*args, **kwargs)

    def get_positions(self):
        return self.positions.all()

    def get_absolute_url(self):
        return reverse("sales:details", kwargs={"pk": self.pk}) #The first argument refers to 'first_arg:name' of the path() in urls.py
    


class CSV(models.Model):
    file_name = models.CharField(max_length=120, null=True)
    csv_file = models.FileField(upload_to='csvs', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.file_name