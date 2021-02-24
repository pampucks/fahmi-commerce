"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#import settings dan static diperlukan untuk serving staticfiles dalam lingkup development
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
#menggunakan views dari app products sebagai homepage.
from products import views as productsViews
from carts import views as cartsViews
from orders import views as ordersViews
from accounts import views as accountsViews
from marketing import views as marketingViews

urlpatterns = [
    path('', productsViews.home, name='home'),
    path('s/', productsViews.search, name='search'),
    path('products/', productsViews.all, name='products'),
    path('products/<slug>/', productsViews.single, name='single_product'),
    path('cart/', cartsViews.view, name='cart'),
    path('cart/<slug>/', cartsViews.add_to_cart, name='add_to_cart'),
    path('cart/slug/<id>/', cartsViews.remove_from_cart, name='remove_from_cart'),
    path('checkout/', ordersViews.checkout, name='checkout'),
    path('checkout/proceed_checkout/', ordersViews.proceed_checkout, name='proceed_checkout'),
    path('orders/', ordersViews.orders, name='user_orders'),
    path('ajax/dismiss_marketing_message/', marketingViews.dismiss_marketing_message, name='dismiss_marketing_message'),
    path('ajax/email_signup/', marketingViews.email_signup, name='ajax_email_signup'),
    path('ajax/add_user_address/', accountsViews.add_user_address, name='ajax_add_user_address'),

    path('admin/', admin.site.urls),
    path('accounts/login/', accountsViews.login_view, name='auth_login'),
    path('accounts/logout/', accountsViews.logout_view, name='auth_logout'),
    path('accounts/register/', accountsViews.registration_view, name='auth_register'),
    path('accounts/activate/<activation_key>/', accountsViews.activation_view, name='activation_view'),
    
] 


#if setting.debug, jika debug=True maka urlpatterns akan ditambahkan static_root dan media_root.
#dengan begitu proses serving staticfiles bisa berjalan
#hal ini tidak direkomendasikan JIKA sedang berada dalam lingkup produksi atau deployment
#dan ketika dalam lingkup deployment, debug harus False.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
