from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Profile, Comments, Image
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import NewCommentForm, NewImageForm, EditProfileForm, EditUserForm, SignUpForm
from django.contrib.auth.models import User
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth import login


# View Function to display the timeline
@login_required(login_url='login')
def timeline(request):
    current_user = request.user
    posts = Image.get_images()
    return render(request, 'all/timeline.html', {"current_user": current_user, "posts": posts})

# View Function to display a user's profile
@login_required(login_url='login')
def other_profile(request, user_id):
    try:
        # current_user.id=request.user.id
        profile = Profile.objects.all().filter(user=user_id)
        print(profile)
        photos = Image.objects.filter(user_id=user_id)
    except Image.DoesNotExist:
        raise Http404()
    return render(request, 'all/userprofile.html', {"profile": profile, "photos": photos})

#View function to view my profile
@login_required(login_url='login')
def my_profile(request):
    current_user = request.user
    profile = Profile.objects.filter(user = current_user)
    image = Image.objects.filter(user = current_user)
    return render(request, 'all/myprofile.html', {"profile": profile, "images": image})

#View function to search for users in the app
@login_required(login_url='login')
def search_results(request):
    if 'user' in request.GET and request.GET["user"]:
        search_term = request.GET.get("user")
        profiles = Profile.search_profile(search_term)
        message = f"{search_term}"

        return render(request, 'all/search.html', {"message": message, "profiles": profiles})

    else:
        message = "You haven't searched for any user"
        return render(request, 'all/search.html', {"message": message})

#View function to comment on any image
@login_required(login_url='login')
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
@login_required(login_url='login')
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
@login_required(login_url='login')
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


@login_required(login_url='login')
def like(request):
    '''
    The view starts by looking for a GET variable called id. If it finds one, it retrieves the
    Image object that is associated with this id.
    Next, the view checks to see whether the user has voted for this bookmark before.
    This is done by calling the filter method.
    If this is the first time that the user has liked for this bookmark, we increment the
    post.likes
    '''
    if request.GET['id']:
        try:
            id = request.GET['id']
            post = Image.objects.get(id=id)
            user_liked = post.users_liked.filter(
                username=request.user.username)
            if not user_liked:
                post.likes += 1
                post.users_liked.add(request.user)
                post.save()

            elif user_liked and post.likes != 0:
                post.likes -= 1
                post.users_liked.remove(request.user)
                post.save()
        except ObjectDoesNotExist:
            raise Http404('Post not found.')

    if request.META['HTTP_REFERER']:
        return HttpResponseRedirect(request.META['HTTP_REFERER'], {"user_liked": user_liked})

    return HttpResponseRedirect('/')



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('various')
    else:
        return render(request, 'registration/account_activation_invalid.html')
