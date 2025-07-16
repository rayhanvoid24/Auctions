from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_item/", views.create_listing, name= "create"),
   path("listing/<int:list_id>/", views.listing, name="listing"),
   path("watchlist/", views.watchlist, name= "watchlist")

]  
