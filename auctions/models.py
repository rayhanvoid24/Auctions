from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watch_list = models.ManyToManyField('auction_list', related_name='watched_by') ##the User model has a .watch_list connection,That gives you access to full auction_list objects,
    ##such as image or description##
    
    
    pass


class auction_list(models.Model):

    category_choices= [

    ('electronics', 'Electronics'),
    ('books', 'Books'),
    ('games', 'Games'),
    ('clothing', 'Clothing'),
    ('cricket_gear', 'Cricket Gear')

    ]
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    item= models.CharField(max_length= 30)
    category= models.CharField(max_length= 20, choices= category_choices)
    description= models.CharField(max_length= 300)
    price= models.DecimalField(max_digits= 10, decimal_places= 2,blank= True,null= True)
    image= models.ImageField(upload_to='listing_images/',blank=True, null= True)
    starting_bid = models.DecimalField(max_digits= 10,decimal_places= 2, blank= True)
    created= models.DateTimeField(auto_now_add= True)
    winner= models.ForeignKey(User, on_delete= models.SET_NULL, blank=True,null= True,related_name= "won_auction")
    is_closed= models.BooleanField(default= False)
    
    def __str__(self):
         return f'{self.item} by {self.user.username}'

    

class Bid(models.Model):
        user= models.ForeignKey(User,on_delete= models.CASCADE)
        amount= models.DecimalField(max_digits= 10, decimal_places=2,)
        auction= models.ForeignKey(auction_list, on_delete= models.CASCADE)
        

        def __str__ (self):
             return f'{self.amount} on {self.auction} by {self.user.username}'




class Comment(models.Model):
     comment = models.TextField(max_length= 300)
     user= models.ForeignKey( User, on_delete= models.CASCADE)
     time= models.DateTimeField( auto_now= True)
     auction= models.ForeignKey(auction_list, on_delete=models.CASCADE)

     def __str__(self):
          return f'{self.user} :{self.comment}'









