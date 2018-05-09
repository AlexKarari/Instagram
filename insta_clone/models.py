from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    avatar = models.ImageField(upload_to='profilepicture/', blank=True)
    bio = models.CharField(max_length=1000)
    user = models.ForeignKey(User)

class Comments(models.Model):
    comment = models.CharField(max_length=1000)
    comment_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['comment_time']
        

class Image(models.Model):
    image = models.ImageField(upload_to='picfolder/')
    image_name = models.CharField(max_length=30)
    image_caption = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile)
    likes = models.IntegerField(default=0)
    comments = models.ForeignKey(Comments)
    date_uploaded = models.DateTimeField(auto_now_add=True, blank=True)
    
    class Meta:
        ordering = ['-date_uploaded']
    
    def save_image(self):
        self.save()

