from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Bid(models.Model):
    bid = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='bidder')
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bid}"


class Listing(models.Model):
    category = models.CharField(max_length=35, null=True, blank=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=900)
    pic = models.URLField(null=True, blank=True)
    date_listed = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)
    current_bid = models.ForeignKey(Bid, on_delete=models.CASCADE,
                                    default=None, related_name='bid_listing')
    lister = models.ForeignKey(User, on_delete=models.CASCADE, default=None,
                               related_name='user_listing')
    watchlist = models.ManyToManyField(
        User, blank=True, related_name='watched_listings')

    def __str__(self):
        return f"Title:{self.title}\nListed by:{self.lister}"


class Comment(models.Model):
    comment = models.CharField(max_length=900)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='Listing_commenter')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
                                related_name='listing_comments', default=None)

    def __str__(self):
        return f"Comment by {self.commenter} for {self.listing}:\n{self.comment}"
