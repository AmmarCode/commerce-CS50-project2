from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bid, Comment, Listing, User


def index(request):
    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


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


def view_category(request):
    listings = Listing.objects.all()
    categories = []
    for listing in listings:
        if listing.category not in categories:
            categories.append(listing.category)
    return render(request, "auctions/category.html", {
        "categories": categories
    })


def listings_by_category(request, category):
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def closed_listings(request):
    listings = Listing.objects.filter(active=False)
    return render(request, "auctions/closed_listings.html", {
        "listings": listings
    })


@login_required
def create_listing(request):
    if request.method == "POST":
        category = request.POST['category']
        title = request.POST['title']
        description = request.POST['description']
        pic = request.POST['pic']
        date_listed = request.POST['date_listed']
        current_bid = request.POST['current_bid']
        lister = request.user

        bid = Bid(bid=current_bid, bidder=lister)
        listing = Listing(category=category, title=title,
                          description=description, pic=pic,
                          date_listed=date_listed, 
                          current_bid=bid, 
                          active=True, lister=lister)

        bid.save()
        listing.save()

        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listing.html")


@login_required
def view_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watched = request.user in listing.watchlist.all()
    comments = listing.listing_comments.all()
    author = request.user.username == listing.lister.username
    return render(request, "auctions/view_listing.html", {
        "listing": listing,
        "watched": watched,
        "comments": comments,
        "author": author
    })


@login_required
def place_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bid = float(request.POST['bid'])
    if bid > listing.current_bid.bid:
        new_bid = Bid(bid=float(bid), bidder=request.user)
        new_bid.save()

        listing.current_bid = new_bid
        listing.save()
        return render(request, "auctions/view_listing.html", {
            "listing": listing,
            "message": "Bid updated successfully",
            "updated": True,
        })
    else:
        return render(request, "auctions/view_listing.html", {
            "listing": listing,
            "message": "Your bid have to be greater than the current bid, pease try again",
            "updated": False,
        })


@login_required
def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))


@login_required
def watch(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))


@login_required
def unwatch(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))


@login_required
def view_watchlist(request):
    user = request.user
    listings = user.watched_listings.all()
    return render(request, "auctions/view_watchlist.html", {
        "listings": listings
    })


@login_required
def comment(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    comment = request.POST['comment']
    comm = Comment(comment=comment, commenter=user, listing=listing)
    comm.save()
    return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))
