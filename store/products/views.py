from django.shortcuts import redirect, render, HttpResponseRedirect
from products.models import ProductCategory, Product, Basket
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    context = {
        'title': 'Store'
    }
    return render (request, 'products/index.html', context)


def products(request, category_id=None, page=1):
    context = {'title': 'Каталог', 'categories': ProductCategory.objects.all()}
    if category_id:
        products =Product.objects.filter(category_id=category_id)
        
    else:
        products = Product.objects.all()
    paginator = Paginator(products, 1)
    products_paginator = paginator.page(page)
    context.update({'products': products_paginator})
    return render (request, 'products/products.html', context)

@login_required
def basket_add(request, product_id):
    current_page = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
        return HttpResponseRedirect(current_page)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(current_page)

@login_required   
def basket_delete(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def like_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.likes += 1
    product.save()
    return redirect('products:product_detail', product_id=product.id)

def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'products/product_detail.html', {'product': product})
