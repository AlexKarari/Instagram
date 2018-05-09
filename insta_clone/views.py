from django.shortcuts import render
from .models import Profile, Comments, Image

# View Function to display a user's profile
def profile(request):
    prof_pic = Profile.objects.all()
    return render(request, 'all/profile.html', {'avatar': prof_pic})
