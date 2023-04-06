from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, AuctionListing, Bid, Comment, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.filter(status="open")
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


@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        img = request.POST["img"]
        
        category_id = request.POST["category"]
        category = Category.objects.get(pk=category_id)

        owner = request.user

        listing = AuctionListing(title=title, description=description, starting_bid=starting_bid, img=img, category=category, owner=owner)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "auctions/create_listing.html", {
        "categories": Category.objects.all()
    })


def listing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)

    # number of bids
    num_bids = listing.bids.count()

    # check if current listing is already in the users watchlist
    in_watchlist = False
    watchlists = Watchlist.objects.filter(user=request.user)
    for watchlist in watchlists:
        if watchlist.listing == listing:
            in_watchlist = True

    # comments
    comments = Comment.objects.filter(listing=listing)
        
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "in_watchlist": in_watchlist,
        "num_bids": num_bids,
        "comments": comments
    })


@login_required
def add_to_watchlist(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = AuctionListing.objects.get(pk=listing_id)
        user = request.user

        watchlist = Watchlist(user=user, listing=listing)
        watchlist.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


@login_required
def remove_from_watchlist(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = AuctionListing.objects.get(pk=listing_id)
        
        watchlist = Watchlist.objects.get(listing=listing)
        watchlist.delete()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


@login_required
def bid(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = AuctionListing.objects.get(pk=listing_id)

        bid_amount = float(request.POST["bid_amount"])
        
        user = request.user

        if bid_amount >= listing.starting_bid and bid_amount > listing.highest_bid:
            listing.highest_bid = bid_amount
            listing.winner = user
            listing.save()

            bid = Bid(listing=listing, bid_amount=bid_amount, bidder=user)
            bid.save()
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
        else:
            return render(request, "auctions/bid_error.html")


@login_required
def close_bid(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = AuctionListing.objects.get(pk=listing_id)
        listing.status = "closed"
        listing.save()

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


@login_required
def watchlists(request):
    user = request.user
    watchlists = Watchlist.objects.filter(user=user)

    return render(request, "auctions/watchlists.html", {
        "watchlists": watchlists
    })


@login_required
def add_comment(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = AuctionListing.objects.get(pk=listing_id)

        content = request.POST["content"]

        owner = request.user

        comment = Comment(content=content, owner=owner, listing=listing)
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def categories(request):
    categories = Category.objects.all()

    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category_detail(request, category_id):
    category = Category.objects.get(pk=category_id)

    listings = category.listings.filter(status="open")
        
    return render(request, "auctions/category_detail.html", {
        "category": category,
        "listings": listings
    })