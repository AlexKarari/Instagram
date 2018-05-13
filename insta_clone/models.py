from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="profpic/", blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_profiles(cls):
        profiles = cls.objects.all()
        return profiles

    @classmethod
    def get_other_profiles(cls, user_id):
        profiles = Profile.objects.all()
        other_profiles = []
        for profile in profiles:
            if profile.user.id != user_id:
                other_profiles.append(profile)
                return other_profiles

# Create Profile when creating a User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Save Profile when saving a User
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    def save_tag(self):
        self.save()

    def delete_tag(self):
        self.delete()

    @classmethod
    def get_tags(cls):
        tags_available = cls.objects.all()
        return tags_available


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="picfolder/")
    caption = models.TextField(blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True) 
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-date_posted']

    @classmethod
    def get_posts(cls):
        posts = cls.objects.all()
        return posts

    @classmethod
    def get_profile_posts(cls, profile_id):
        profile_posts = Post.objects.filter(profile=profile_id).all()
        return profile_posts


class Follow(models.Model):
    user = models.ForeignKey(User)
    profile = models.ForeignKey(Profile)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_following(cls, user_id):

        following = Follow.objects.filter(user=user_id).all()

        return following


class Comments(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_post_comments(cls, post_id):
        comments = Comment.objects.filter(post=post_id)
        return comments


class Like(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_post_likes(cls, post_id):
        post_likes = Like.objects.filter(post=post_id)
        return post_likes

    @classmethod
    def num_likes(cls, post_id):
        post = Like.objects.filter(post=post_id)
        found_likes = post.aggregate(
            Sum('likes_number')).get('likes_number__sum', 0)

        return found_likes
