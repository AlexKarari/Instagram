from django.shortcuts import render
from .models import Profile, Comments, Image

# View Function to display a user's profile
def profile(request):
    prof_pic = Profile.objects.all()
    return render(request, 'all/profile.html', {'avatar': prof_pic})

#View function to search for users in the app
def search_results(request):
    if 'user' in request.GET and request.GET["user"]:
        search_term = request.GET.get("user")
        searched_articles = Profile.search_profile(search_term)
        message = f"{search_term}"

        return render(request, 'all/search.html', {"message": message, "articles": searched_articles})

    else:
        message = "You haven't searched for any user"
        return render(request, 'all/search.html', {"message": message})
