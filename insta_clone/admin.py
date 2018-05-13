from django.contrib import admin
from .models import Profile, Comments, Tag, Post, Follow, Like

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

admin.site.register(Profile)
admin.site.register(Comments)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Follow)
admin.site.register(Like)
