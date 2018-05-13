from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Profile, Comments, Image
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .forms import NewCommentForm, NewImageForm, EditProfileForm, EditUserForm
from django.contrib.auth.models import User

# View Function to display the timeline
# @login_required(login_url='/accounts/login/')
def timeline(request):
    current_user = request.user
    posts = Image.get_images()
    return render(request, 'all/timeline.html', {"current_user": current_user, "posts": posts})

# View Function to display a user's profile
# @login_required(login_url='/accounts/login/')
def user_profile(request, user_id):
    try:
        profile = Profile.objects.filter(id=user_id)
        photos = Image.objects.filter(user_id=user_id)
    except Image.DoesNotExist:
        raise Http404()
    return render(request, 'all/userprofile.html', {"profile": profile, "photos": photos})

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
# @login_required(login_url='/accounts/login/')
def comment(request, id):
    title = 'IG clone | Comments'
    post = get_object_or_404(Image, id=id)
    current_user = request.user
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.photo = post
            comment.save()

            return redirect('various')
    else:
        form = NewCommentForm()

    return render(request, 'new_comment.html', {"title": title, "form": form})

#View function to upload a new image
# @login_required(login_url='/accounts/login/')
def new_photo(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewImageForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = current_user
            photo.save()
            return redirect('various')
    else:
        form = NewImageForm()
    return render(request, 'newimage.html', {"form": form})

#View function to edit out one's profile
# @login_required(login_url='/accounts/login/')
@transaction.atomic
def editprofile(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('various')
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)
    return render(request, 'profilechange.html', {"user_form": user_form, "profile_form": profile_form})
