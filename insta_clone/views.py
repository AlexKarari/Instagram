from django.shortcuts import render
from .models import Profile, Comments, Image
from django.contrib.auth.decorators import login_required

# View Function to display the timeline
@login_required(login_url='/accounts/login/')
def timeline(request):
    current_user = request.user
    images = Image.objects.order_by('-date_uploaded')
    profile = Profile.objects.order_by('-date_created')
    comment = Comments.objects.order_by('-comment_time')
    return render(request, 'all/timeline.html', {'image':images, 'name':profile, 'comment':comment})


# View Function to display a user's profile
@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    prof_pic = Image.objects.get(user_id=current_user.id)
    profile = Profile.objects.get(user_id=current_user.id)
    prof_images = Image.objects.all().filter(profile_id=current_user.id)
    return render(request, 'all/profile.html', {'avatar': prof_pic, 'name':profile, 'image':prof_images})

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
