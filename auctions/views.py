from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Comment
from .forms import NewListingForm, NewCommentForm


def index(request):
    listings = Listing.objects.all().order_by('-creation_date')
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = Listing()
            listing.title = form.cleaned_data['title']
            listing.description = form.cleaned_data['description']
            listing.price = form.cleaned_data['starting_bid']
            imageURL = ""
            listing.category = form.cleaned_data['category']
            if request.POST.get('imageURL'):
                imageURL = form.cleaned_data['imageURL']
            else :
                imageURL = "https://wallpaperaccess.com/full/1605486.jpg"
            listing.imageURL = imageURL
            listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
                return render(request, "auctions/create_listing.html")
    else:
        return render(request, "auctions/create_listing.html", {
            "form": NewListingForm(),
        })
def wishlist_view(request, username):
    return render(request, "auctions/wishlist.html", {
        "username": username,
        "listings": Listing.objects.filter(user__username=username)
    })

def create_comment(request, listing):
    listing = Listing.objects.get(title=listing)
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data['body']
            comment = Comment(listing=listing, name=name, body=body)
            comment.save()
            return HttpResponseRedirect(f'/listing/{listing}')
        else:
                return render(request, "auctions/create_comment.html", {
                    "form": form,
                    "listing": listing,
                })
    else:
        return render(request, "auctions/create_comment.html", {
        "form": NewCommentForm(),
        "listing": listing,
        })

def listing_view(request, listing):
    listing = Listing.objects.get(title=listing)
    wishlist_items = Listing.objects.filter(user=request.user)
    exists = False
    if listing in wishlist_items:
        exists = True
    return render(request, "auctions/listing_view.html", {
        "listing": listing,
        "exists": exists,
    })

def categories(request):
    return render(request, "auctions/categories.html",{
        "categories": ['No Category', 'Fashion', 'Sport', 'Electronics', 'Accesories'],
    })

def category_view(request, category):
    listings = Listing.objects.filter(category=category).order_by('-creation_date')
    return render(request, "auctions/category_view.html", {
        "category": category,
        "listings": listings,
    })


def addwishlist(request, listing):
    if request.user.username:
        user = User.objects.get(username=request.user)
        listing = Listing.objects.get(title=listing)
        user.listings.add(listing)
        return HttpResponseRedirect(f'/listing/{listing}')
    else:
        return HttpResponseRedirect(f'/listing/{listing}')

def removewishlist(request, listing):
    if request.user.username:
        user = User.objects.get(username=request.user)
        listing = Listing.objects.get(title=listing)
        user.listings.remove(listing)
        return HttpResponseRedirect(f'/listing/{listing}')
    else:
        return HttpResponseRedirect(f'/listing/{listing}')


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
