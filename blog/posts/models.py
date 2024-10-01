from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=75)
    body  = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(default='fallback.png',blank=True)
    auther = models.ForeignKey(User, on_delete=models.CASCADE,default=None) #on delete is requirecd telling the database how to handle if the relationship or user is delete, casecade will delete all post made by a user if the user is deleted or removed
    
    def __str__(self):
        return self.title


     

class Members(models.Model):
    username = models.CharField(max_length=75)
    email = models.CharField(max_length=200,null=True)
    avatar = models.ImageField(null=True)
    age = models.IntegerField()
    posts = models.ManyToManyField(Post,blank=True,related_name="members")
    created_at = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    updated_at = models.DateTimeField(auto_now = True, null=True)

    class Meta:
        ordering = ['-updated_at','-created_at']

    def __str__(self):
        return self.username



class Address(models.Model):
    member_id  = models.OneToOneField(Members,on_delete=models.CASCADE,default=None)
    street = models.CharField(max_length=75)
    city = models.CharField(max_length=75)
    country  = models.CharField(max_length=75)

    def __str__(self):
        return self.street