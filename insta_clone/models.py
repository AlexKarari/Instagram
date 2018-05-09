from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    avatar = models.ImageField(upload_to='profilepicture/', blank=True)
    bio = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profile(cls):
        profile = cls.objects.all()
        return profile
    @classmethod
    def search_profile(cls, search_term):
        profile = cls.objects.filter(user_icontains=search_term)
        return profile
    

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

