from django.shortcuts import render, Http404

# Create your views here.

from .models import Product, ProductImage
from marketing.models import MarketingMessage, Slider
from marketing import middleware

def home(request):
    #untuk testing user login
    # if request.user.is_authenticated:
    #     username_is = 'fahmi'
    #     context = {'username_is': request.user}
    # else:
    #     context = {'username_is': request.user}
    sliders = Slider.objects.all_featured()
    products = Product.objects.all()
    # marketing_message = MarketingMessage.objects.all()[0]
    context = {
        'products': products,
        'sliders': sliders,
        # 'marketing_message': marketing_message,
    }
    #konfigurasikan dulu templates_dirs di settings, baru bisa menggunakan template.
    template = 'products/home.html' 
    return render(request, template, context)


def all(request):
    products = Product.objects.all()
    # marketing_message = MarketingMessage.objects.all()[0]
    context = {
        'products': products,
        # 'marketing_message': marketing_message,
    }
    template = 'products/all.html'
    return render(request, template, context)


def single(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        # marketing_message = MarketingMessage.objects.all()[0]
        images = ProductImage.objects.filter(product=product)
        context = {
            'product': product, 
            'images': images,
            # 'marketing_message': marketing_message,
        }
        template = 'products/single.html'
        return render(request, template, context)
    except:
        raise Http404

def search(request):
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        products = Product.objects.filter(title__icontains=q)
        # marketing_message = MarketingMessage.objects.all()[0]
        context = {
            'query': q, 
            'products': products,
            # 'marketing_message': marketing_message,
        }
        template = 'products/results.html'
    else:
        context = {}
        template = 'products/home.html'
    
    return render(request, template, context)
    