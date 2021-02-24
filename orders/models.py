from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
from carts.models import Cart

User = get_user_model()

STATUS_CHOICES = (
    ("Started", "Started"),
    ("Abandoned", "Abandoned"),
    ("Finished", "Finished"),
)


class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120, default='ABC', unique=True)
    cart = models.ForeignKey("carts.Cart", on_delete=models.CASCADE)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default='Started')
    #address
    sub_total = models.IntegerField(null=True, blank=True)
    tax_total = models.IntegerField(null=True, blank=True)
    final_total = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.order_id
    