from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse


from myapp.form import CustomUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
from myapp import views



def members(request):
    products=Products.objects.filter(trending=1)
    return render(request,'index.html',{"products":products})


def collections(request):
    catagory = Catagory.objects.filter(status=0)
    return render(request,'collections.html',{"catagory":catagory})
def collectionviews(request,name):
        if(Catagory.objects.filter(name=name,status=0)):

            products = Products.objects.filter(category__name=name)
            return render(request,'product.html',{"products":products,"category_name":name})
        else:
             messages.warning(request,"no such products")
             return redirect("collections")
def product_details(request,cname,pname):
     if(Catagory.objects.filter(name=cname,status=0)):
          
          if(Products.objects.filter(name=pname,status=0)):
               products=Products.objects.filter(name=pname,status=0).first()
               return render(request,"product_details.html",{"products":products})
          else:
               messages.error(request,"no such catagory found")
               return redirect("collections")
     else:
          messages.error(request,"no such catagory found")
          return redirect("collections")

     
def login_page(request):
     if request.user.is_authenticated:
          
          return redirect("/")
     else:
        

        if request.method=='POST':
          name=request.POST.get('username')
          pwd=request.POST.get('password')
          user=authenticate(request,username=name,password=pwd)
          if user is not None:
               login(request,user)
               messages.success(request,"logged in successfully")
               return redirect("/")
          else:
               messages.error(request,"invalid username or password")
               return redirect("/login")

     return render(request,"login.html")
def add_to_cart(request):
     if request.headers.get('x-requested-with')=='XMLHttpRequest':
          if request.user.is_authenticated:
               data=json.load(request)
               product_qty=data['product_qty']
               product_id=data['pid']
               #print(request.user.id)
               product_status=Products.objects.get(id=product_id)
               if product_status:
                    if Cart.objects.filter(user=request.user,product_id=product_id):

                         return JsonResponse({'status':"product already in cart"},status=200)
                    
                    else:
                    
                         if product_status.quantity>=product_qty:
                              Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                              return JsonResponse({'status':"product added to cart"},status=200)
                         else:
                              return JsonResponse({'status':"product stock not available"},status=200)
               else:

                    return JsonResponse({'status':"login to add to cart"},status=200)
          else:
               return JsonResponse({'status':"invalid access"},status=200)
def cart_page(request):
     if request.user.is_authenticated:
          cart=Cart.objects.filter(user=request.user)
          return render(request,"cart.html",{"cart":cart})
     else:
          return redirect("/")
def remove_cart(request,cid):
     cartitem=Cart.objects.get(id=cid)
     cartitem.delete()
     return redirect("/cart")
def fav_page(request):
     if request.headers.get('x-requested-with')=='XMLHttpRequest':
          if request.user.is_authenticated:
               data=json.load(request)
               product_id=data['pid']
               product_status=Products.objects.get(id=product_id)
               if product_status:
                    if Favourite.objects.filter(user=request.user,product_id=product_id):
                        
                         return JsonResponse({'status':"Product Already in favourite"},status=200)
                    else:
                         Favourite.objects.create(user=request.user,product_id=product_id)
                         return JsonResponse({'status':"Product Added to favourite"},status=200)

              
          else:
               return JsonResponse({'status':"login to add to favourite"},status=200)
     else:
          return JsonResponse({'status':"invalid access"},status=200)
def favviewpage(request):
     if request.user.is_authenticated:
          fav=Favourite.objects.filter(user=request.user)
          return render(request,"fav.html",{"fav":fav})
     else:
          return redirect("/")
def remove_fav(request,fid):
      
      
      item=Favourite.objects.get(id=fid)
      item.delete()
      return redirect("/favviewpage")
def register(request):
     form=CustomUserForm()
     if request.method=='POST':
          form=CustomUserForm(request.POST)
          if form.is_valid():
               form.save()
               messages.success(request,"Registered successfully you can login now...!")
               return redirect("/login")

    
     
     return render(request,"register.html",{"form":form})   
def logout_page(request):
     if request.user.is_authenticated:
          logout(request)
          messages.success(request,"logged out successfully")
          return redirect("/")




               
               
               

                    
             

     
    




# Create your views here.
