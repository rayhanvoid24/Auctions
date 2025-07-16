from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, auction_list,Comment,Bid

def index(request):
    # Show only open auctions OR closed ones without a winner
    product = auction_list.objects.filter(
        is_closed=False
    ) | auction_list.objects.filter(
        is_closed=True, winner__isnull=True
    )

    return render(request, "auctions/index.html", {
        "products": product.distinct()  # just in case
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


def create_listing(request):
         categories= auction_list.category_choices

         if request.user.is_authenticated and request.method== "POST":
             try: 
                 new_list= auction_list(
                 item= request.POST.get("item"),
                 description= request.POST.get("Description"),
                 image= request.FILES.get("image"),
                 category = request.POST.get("category"),
                 starting_bid= request.POST.get("starting_bid"),
                 user= request.user)

                 new_list.save()
                 return redirect("index")
             
             except Exception as e:
                 return render(request, "auctions/create.html", {
                "categories": categories,
                "error": f"Error creating listing: {str(e)}"
            })
             
         return render(request, "auctions/create.html", {
          "categories": categories,
          })

@login_required 
def listing (request, list_id):
    auction = get_object_or_404(auction_list, id=list_id)
    comments = Comment.objects.filter(auction=auction).order_by('-time')
    bids = Bid.objects.filter(auction=auction).order_by('-amount')
    is_watching = request.user.watch_list.filter(id=auction.id).exists()
    highest_bid= bids.first().amount if bids.exists() else auction.starting_bid
    top_bid= bids.first()
    
    if request.method== "POST":
       comment_text = request.POST.get("comment") 
       

       if comment_text:
           Comment.objects.create (
               comment= comment_text,
               user= request.user,
               auction= auction
           )

    if "bid" in request.POST:
         if auction.is_closed:
            messages.error(request, "This auction is closed. No more bids are allowed.")
         else:
           bid_input = request.POST.get("bid")
         
         if bid_input:
            try: 
              bid_amount= float(bid_input)
              
              if bid_amount > highest_bid:
                    Bid.objects.create(
                   amount= bid_amount,
                   user= request.user,
                   auction= auction

              )   
              else:
               messages.error(request,"your bid must be higher ")
            except ValueError: 
              messages.error(request, "plesse enter a valid number")

    if "toggle_watch" in request.POST and auction.is_closed== False:
        if is_watching:
                request.user.watch_list.remove(auction)
        else:
                request.user.watch_list.add(auction)

        return redirect("listing", list_id=list_id)
    
    if request.user == auction.user:
     if "close_auction" in request.POST:
        if not auction.is_closed:
            top_bid = bids.first()
            if top_bid:
                auction.winner = top_bid.user
            auction.is_closed = True
            auction.save()



            

           
    return render(request,"auctions/listing.html", {
           "auction": auction,
           "comments": comments,
            "bids": bids,
            "is_watching": is_watching

              })
   

@login_required
def watchlist(request):
    watch_list= request.user.watch_list.all()
    return render(request, "auctions/watchlist.html",{
        "watch_item": watch_list
    })


