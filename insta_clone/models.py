from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    avatar = models.ImageField(
        upload_to='profilepicture/', null=True, blank=True)
    bio = models.TextField()

    def __str__(self):
        return self.user.username
        
    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def update_profile(cls, id, bio):
        update = Image.objects.filter(id=id).update(bio=bio)
        return update

    @classmethod
    def search_profile(cls, search_term):
        profile = cls.objects.filter(user__username__icontains=search_term)
        return profile



class Image(models.Model):
    image = models.ImageField(upload_to='picfolder/', blank=True, null=True)
    image_name = models.CharField(max_length = 100, blank=True)
    image_caption = models.CharField(max_length=100, null=True)
    profile = models.ForeignKey(
        Profile, related_name="user_profile")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    users_liked = models.ManyToManyField(User, related_name="user_liked")
    date_uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_uploaded']

    def __str__(self):
        return self.image
                
    def save_image(self):
        self.save()

    @classmethod
    def get_images(cls):
        images = Image.objects.all()
        return images


class Comments(models.Model):
    comment = models.CharField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    comment_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_time']

    def save_comment(self):
        self.save()

    def __str__(self):
        return self.comment


    def delete_comment(self):
            self.delete()


def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
