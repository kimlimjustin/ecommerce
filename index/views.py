from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from .models import User, Items
import json

#Home page
def index(request):
    return render(request, "index/index.html")

def login_view(request):
    #Check if the user is logged in
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        # if user authentication success
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "index/login.html", {
                "message": "Invalid username and/or password"
            })
    return render(request, "index/login.html")

def register(request):
    #Check if the user is logged in
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]
        email = request.POST["email"]
        confirmation = request.POST["confirmation"]
        #check if the password is the same as confirmation
        if password != confirmation:
            return render(request, "index/register.html", {
                "message": "Passwords must match."
            })
        #Checks if the username is already in use
        try:
            user = User.objects.create_user(username = username, password = password, email = email)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        except IntegrityError:
            return render(request, "index/register.html", {
                "message": "Username already taken"
            })
    return render(request, "index/register.html")


def logout_view(request):
    #Logout the user
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def sell_item(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == "POST":
        name = request.POST["item-name"]
        description = request.POST["item-description"]
        image = request.FILES["image"]
        price = int(request.POST["price"])
        #if user send negative price
        if price < 0:
            return render(request, "index/create.html", {
                "message": "Invalid price"
            })
            #save the item
        item = Items(name = name, description = description, image = image, seller = request.user, price = price)
        item.save()
        #redirect to the product page
        return HttpResponseRedirect(reverse('item', args = [item.pk]))
    return render(request, "index/create.html")

def item(request, id):
    item = Items.objects.filter(id = id)
    if item.count() == 0:
        #404 Item not found.
        return HttpResponseRedirect(reverse('404'))
    else: item = item[0]
    liked = item.likes.filter(pk = request.user.pk).count() > 0
    total_like = item.likes.all().count()
    saved = request.user.cart.filter(pk = item.pk).count() > 0
    return render(request, "index/item.html", {
        "item": item,
        "liked": liked,
        "total_like": total_like,
        "saved": saved
        })

def edit_item(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    item = Items.objects.filter(id = id)
    if item.count() == 0:
        #404 Item not found.
        return HttpResponseRedirect(reverse('404'))
    else: item = item[0]
    if request.method == "POST":
        item.image.delete()
        item.image = request.FILES["image"]
        item.name = request.POST["item-name"]
        item.description = request.POST["item-description"]
        item.price = request.POST["price"]
        item.save()
        return HttpResponseRedirect(reverse('item', args = [item.pk]))
    # Check if seller is the user
    if item.seller != request.user:
        return HttpResponse(status = 403)
    else:
        return render(request, "index/edit_item.html", {
            "item": item
        })

def delete_item(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    item = Items.objects.filter(id = id)
    if item.count() == 0:
        #404 Item not found.
        return HttpResponseRedirect(reverse('404'))
    else: item = item[0]
    if item.seller != request.user:
        return HttpResponse(status = 403)
    else:
        print(request.method)
        if request.method == "POST":
            item.delete()
            return HttpResponseRedirect(reverse('index'))

# Like api
def like(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    data = json.loads(request.body)
    item = Items.objects.filter(id = data["id"])
    if item.count() == 0:
        #404 Item not found.
        return HttpResponseRedirect(reverse('404'))
    else: item = item[0]
    if request.method == "POST":
        liked = item.likes.filter(pk = request.user.pk).count() > 0
        #Check if the user liked it
        if not liked:
            item.likes.add(request.user)
            item.save()
        return JsonResponse({"message": "Success"})

# Unlike api
def unlike(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    data = json.loads(request.body)
    item = Items.objects.filter(id = data["id"])
    if item.count() == 0:
        #404 Item not found.
        return HttpResponseRedirect(reverse('404'))
    else: item = item[0]
    if request.method == "POST":
        item.likes.remove(request.user)
        item.save()
        return JsonResponse({"message": "Success"})

def cart(request):
    items = request.user.cart.all()
    total_price = 0
    for i in items:
        total_price += i.price
    return render(request, "index/cart.html", {
        "items": items,
        "total_price": total_price
    })

def add_to_cart(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    data = json.loads(request.body)
    item = Items.objects.filter(id = data["id"])
    if item.count() == 0:
        #404 Item not found.
        return HttpResponseRedirect(reverse('404'))
    else: item = item[0]
    if request.method == "POST":
        user = User.objects.get(pk = request.user.pk)
        user.cart.add(item)
        user.save()
        return JsonResponse({"message": "Success"})

def remove_from_cart(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    data = json.loads(request.body)
    item = Items.objects.filter(id = data["id"])
    if item.count() == 0:
        #404 Item not found.
        return HttpResponseRedirect(reverse('404'))
    else: item = item[0]
    if request.method == "POST":
        user = User.objects.get(pk = request.user.pk)
        user.cart.remove(item)
        user.save()
        return JsonResponse({"message": "Success"})
        
#Error 404 page
def FourZeroFour(request):
    return render(request, "error/404.html")