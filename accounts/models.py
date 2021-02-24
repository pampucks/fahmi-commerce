from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.db import models
from django.template.loader import render_to_string

from phonenumber_field.modelfields import PhoneNumberField
from localflavor.id_.id_choices import PROVINCE_CHOICES

# Create your models here.
class UserDefaultAddress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping = models.ForeignKey("UserAddress", on_delete=models.CASCADE, null=True, blank=True, related_name="user_address_shipping_default")
    billing = models.ForeignKey("UserAddress", on_delete=models.CASCADE, null=True, blank=True, related_name="user_address_billing_default")

    def __str__(self):
        return self.user.username
    

class UserAddressManager(models.Manager):
    def get_billing_addresses(self, user):
        return super(UserAddressManager, self).filter(billing=True).filter(user=user)


class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    alamat = models.CharField(max_length=120)
    alamat2 = models.CharField(max_length=120, null=True, blank=True)
    kota = models.CharField(max_length=120)
    provinsi = models.CharField(max_length=120, choices=PROVINCE_CHOICES, null=True, blank=True)
    negara = models.CharField(max_length=120)
    kode_pos = models.CharField(max_length=5)
    phone = PhoneNumberField()
    shipping = models.BooleanField(default=True)
    billing = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.user.username

    def get_address(self):
        return "%s, %s, %s, %s, %s" %(self.alamat, self.kota, self.provinsi, self.negara, self.kode_pos)

    objects = UserAddressManager()
    
    class Meta:
        ordering = ['-updated', '-timestamp']


class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return str(self.stripe_id)


class EmailConfirmed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.confirmed)

    def activate_user_email(self):
        activation_url = "%s%s" %(settings.SITE_URL, reverse("activation_view", args=[self.activation_key]))
        context = {
            'activation_key': self.activation_key,
            'activation_url': activation_url,
            'user': self.user.username,

        }
        message = render_to_string('accounts/activation_message.txt', context)
        subject = 'Activate you Email'
        self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.user.email], kwargs)


class EmailMarketingSignUp(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    # confirmed = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    