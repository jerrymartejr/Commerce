from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.utils import timezone


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)
    img = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    img = models.CharField(max_length=1000)
    status = models.CharField(max_length=64, default="open")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="listings")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="listings_won")

    def __str__(self):
        return self.title


class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", null=True)

    def __str__(self):
        return f"{self.listing} - {self.bid_amount} by {self.bidder}"


class Comment(models.Model):
    content = models.CharField(max_length=300)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.owner}: {self.content}"


class Watchlist(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
    listing = models.ForeignKey(AuctionListing, on_delete=models.SET_NULL, null=True, related_name="watchlists")

    def __str__(self):
        return f"{self.listing} - {self.user}"
