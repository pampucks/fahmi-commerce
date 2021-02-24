import time

# import stripe
import midtransclient

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from accounts.forms import UserAddressForm
from accounts.models import UserAddress
from carts.models import Cart
from .models import Order
from .utils import id_generator

# try:
#     stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
#     stripe_secret = settings.STRIPE_SECRET_KEY
# except Exception:
#     print(str(Exception))
#     raise NotImplementedError(str(Exception))

# stripe.api_key = stripe_secret

# Create Snap API instance


def orders(request):

    context = {}
    template = 'orders/user.html'
    return render(request, template, context)


@login_required
def checkout(request):
    
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse('cart'))
    if the_id:
        new_total = 0
        for item in cart.cartitem_set.all():
            line_total = int(item.product.price) * item.quantity
            new_total += line_total

        request.session['items_total'] = cart.cartitem_set.count()

    
    try:
        new_order = Order.objects.get(cart=cart)
    except Order.DoesNotExist:
        new_order = Order()
        new_order.cart = cart
        new_order.user = request.user
        new_order.order_id = id_generator()
        new_order.save()
    except:
        #work on some error message
        return HttpResponseRedirect(reverse('cart'))

    try:
        address_added = request.GET.get("address_added")
        # print(address_added)
    except:
        address_added = None
    
    if address_added is None:
        address_form = UserAddressForm()
    else:
        address_form = None

    current_addresses = UserAddress.objects.filter(user=request.user)
    billing_addresses = UserAddress.objects.get_billing_addresses(user=request.user)
    # print(billing_addresses)
    # ids = request.session['cart_id']
    # total = request.session['items_total'] 


    if request.method == "POST":

    #     param = {
    #         "transaction_details": {
    #             "order_id": ids,
    #             "gross_amount": total
    #         }, "credit_card":{
    #             "secure" : True
    #         }, "customer_details":{
    #             "first_name": "fahmi",
    #             "last_name": "pratama",
    #             "email": "budi.pra@example.com",
    #             "phone": "08111222333"
    #         }
    #     }
            
    # transaction = snap.create_transaction(param)
    
    # transaction_token = transaction['token']

        try:
            user_stripe = request.user.userstripe.stripe_id
            customer = stripe.Customer.retrieve(user_stripe)
            print(customer)
        except:
            pass
        print(request.POST['stripeToken'])

    if new_order.status == "Finished":
        # cart.delete()
        del request.session['cart_id']
        del request.session['items_total']
        return HttpResponseRedirect(reverse('cart'))

    context = {
        "address_form": address_form,
        "current_addresses": current_addresses,
        "billing_addresses": billing_addresses,
        # "stripe_pub": stripe_pub,
    }
    

    # user_stripe = request.user.userstripe.stripe_id
    # customer = stripe.Customer.retrieve(user_stripe)
    snap = midtransclient.Snap(
    # Set to true if you want Production Environment (accept real transaction).
    is_production = False,
    server_key = settings.MIDTRANS_SERVER_KEY,
    client_key= settings.MIDTRANS_CLIENT_KEY
    )
    # Build API parameter
    param = {
        "transaction_details": {
            "order_id": request.session['cart_id'],
            "gross_amount": new_total
        }, 
        "customer_details": {
            "first_name" : request.user.username,
            "email" : request.user.email,


        },
        
        "credit_card":{
            "secure" : True
        }
    }

    transaction = snap.create_transaction(param)

    # transaction_redirect_url = transaction['redirect_url']
    # alternative way to create redirect_url:
    # transaction_redirect_url = snap.create_redirect_url(param)
    # template = 'orders/checkout.html'
    return HttpResponseRedirect(transaction['redirect_url'])




def proceed_checkout(request):
    

    template = 'orders/proceed_checkout.html'
    return render(request, template)