from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("bid", views.bid, name="bid"),
    path("close_bid", views.close_bid, name="close_bid"),
    path("watchlists", views.watchlists, name="watchlists"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category_detail, name="category_detail")
]
