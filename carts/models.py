from django.db import models

from products.models import Product, Variation


class CartItem(models.Model):
    cart = models.ForeignKey("carts.Cart", null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    variations = models.ManyToManyField("products.Variation")
    quantity = models.IntegerField(default=1)
    line_total = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        try:
            return str(self.cart.id)
        except:
            return self.product.title
    

class Cart(models.Model):
    # items = models.ManyToManyField("carts.CartItem")
    # products = models.ManyToManyField("products.Product")
    total = models.IntegerField(null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return "Cart id: %s" %(self.id)
    