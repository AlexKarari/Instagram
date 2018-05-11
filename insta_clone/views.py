from django.shortcuts import render, redirect
from .models import Profile, Comments, Image
from django.contrib.auth.decorators import login_required
from .forms import NewCommentForm, NewStatusForm

# View Function to display the timeline
def timeline(request):
    current_user = request.user
    images = Image.objects.all()
    profile = Profile.objects.all()
    comment = Comments.objects.all()
    return render(request, 'all/timeline.html', {"images": images, "name": profile, "comment": comment})


# View Function to display a user's profile
# @login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    # print(current_user.id)
    # profile = Profile.objects.get(user_id=current_user.id)
    # print(profile)
    prof_pic = Image.objects.all().filter(user_id=current_user.id)
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

#View function to comment on any image
@login_required(login_url='/accounts/login/')
def new_comment(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewCommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.poster = current_user
            comment.save()
        return redirect('various')
    else:
        form = NewCommentForm()
    return render(request, 'new_comment.html', {"form": form})

#View function to put up a new status
# @login_required(login_url='/accounts/login/')
def new_status(request):
    current_user = request.user
    username = current_user.username
    if request.method == 'POST':
        form = NewStatusForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            image.user = request.user
            image.save()
        return redirect('various')
    else:
        form = NewStatusForm()
    return render(request, 'new_status.html', {"form": form})
    
    
#View function to view another user's profile
@login_required(login_url='/ accounts/login/')
def userProfile(request, user_id):
    profile = Profile.objects.get(id=user_id)
    prof_images = Image.objects.all().filter(user_id=user_id)
    return render(request, 'profile.html', {"user": profile, "avatar":prof_images})

#View function to view an individual image for any user
# @login_required(login_url='/ accounts/login/')
def soloImage(request, pic_id):
    image = Image.objects.get(id=pic_id)
    return render(request, 'individual.html', {"image": image})
