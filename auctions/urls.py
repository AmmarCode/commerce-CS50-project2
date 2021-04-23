from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("view_category", views.view_category, name="view_category"),
    path("<int:listing_id>", views.view_listing, name="view_listing"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("view_watchlist", views.view_watchlist, name="view_watchlist"),
    path("<str:category>", views.listings_by_category, name="listings_by_category"),
    path("<int:listing_id>/place_bid", views.place_bid, name="place_bid"),
    path("<int:listing_id>/close_listing", views.close_listing, name="close_listing"),
    path("<int:listing_id>/watch", views.watch, name="watch"),
    path("<int:listing_id>/unwatch", views.unwatch, name="unwatch"),
    path("<int:listing_id>/comment",  views.comment, name="comment"),
]
