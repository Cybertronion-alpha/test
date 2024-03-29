from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Category(models.Model):
    CATEGORY_CHOICES = (
        ("GD", "Graphics & Design"),
        ("DM", "Digital & Marketing"),
        ("VA", "Video & Animation"),
        ("MA", "Music & Audio"),
        ("PT", "Programming & Tech")
    )

    title=models.CharField(max_length=50)
    # image=models.ImageField(upload_to='category')
    slug=models.SlugField(max_length=50)
    parent=models.CharField(max_length=2,choices=CATEGORY_CHOICES,unique=True)
    
    def __str__(self):
        return self.title

class Gigs(models.Model):
    title=models.CharField(max_length=500)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='gig')
    description = models.CharField(max_length=1000)
    price = models.IntegerField(default=5)
    photo = models.FileField(upload_to='gigs')
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# class Transaction(models.Model):
#     buyer=models.ForeignKey(User,on_delete=models.CASCADE)
#     gig=models.ForeignKey(Gigs,on_delete=models.CASCADE)
#     time=models.DateTimeField(default=timezone.now)
#     token=models.CharField(max_length=120)
#     order_id= models.CharField(max_length=120)
#     success=models.BooleanField(default=True)
#     amount=models.DecimalField(max_digits=100,decimal_places=2)

# class Transaction(models.Model):
    # user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    

    # def __str__(self):
    #     return self.gig.title


class Review(models.Model):
    gig = models.ForeignKey(Gigs,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.CharField(max_length=500)

    def __str__(self):
        return self.content

