from django.shortcuts import render,redirect,get_object_or_404
from shop.models import *
from . models import *
from django.core.exceptions import ObjectDoesNotExist

def cart_details(request,total=0,count=0,cart_items=None):
    try:
        ct=CartList.objects.get(cart_id=c_id(request))
        ct_items=ItemList.objects.filter(cart=ct,active=True)
        for i in ct_items:
            total+=(i.prod.price*i.quan)
            count+=i.quan 
    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',{'ci':ct_items,'t':total,'cn':count})

def c_id(request):
   ct_id=request.session.session_key
   if not ct_id:
       ct_id=request.session.create()
   return ct_id

def add_cart(request,product_id):
    prod=Product.objects.get(id=product_id)
    try:
        ct=CartList.objects.get(cart_id=c_id(request))
    except CartList.DoesNotExist:
        ct=CartList.objects.create(cart_id=c_id(request))
        ct.save()
    try:
        c_items=ItemList.objects.get(prod=prod,cart=ct)
        if c_items.quan < c_items.prod.stock:
            c_items.quan+=1
        c_items.save()
    except ItemList.DoesNotExist:
        c_items=ItemList.objects.create(prod=prod,quan=1,cart=ct)
        c_items.save()
    return redirect('cartDetails')


def min_cart(request,product_id):
    ct=CartList.objects.get(cart_id=c_id(request))
    prdt=get_object_or_404(Product,id=product_id)
    c_items=ItemList.objects.get(prod=prdt,cart=ct)
    if c_items.quan>1:
        c_items.quan-=1
        c_items.save()
    else:
        c_items.delete()
    return redirect('cartDetails')


def delete_cart(request,product_id):
    ct=CartList.objects.get(cart_id=c_id(request))
    prdt=get_object_or_404(Product,id=product_id)
    c_items=ItemList.objects.get(prod=prdt,cart=ct)
    c_items.delete()
    return redirect('cartDetails')

