from django.contrib import admin

# Register your models here.
from .models import UserStripe, EmailConfirmed, EmailMarketingSignUp, UserAddress, UserDefaultAddress


admin.site.register(UserStripe)

admin.site.register(EmailConfirmed)

admin.site.register(UserDefaultAddress)


class EmailMarketingSignUpAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'timestamp']
    class Meta:
        model = EmailMarketingSignUp

admin.site.register(EmailMarketingSignUp, EmailMarketingSignUpAdmin)


class UserAddressAdmin(admin.ModelAdmin):
    class Meta:
        model = UserAddress

admin.site.register(UserAddress, UserAddressAdmin)