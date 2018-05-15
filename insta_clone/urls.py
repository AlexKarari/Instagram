from django.conf.urls import url, include
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from insta_clone import views as core_views

urlpatterns = [
    url('^$', views.timeline, name='various'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^userprofile/(\d+)', views.other_profile, name='other_profiles'),
    url(r'^myprofile/', views.my_profile, name='myprofile'),
    url(r'^newphoto/', views.new_photo, name='new_photo'),
    url(r'^comment/(?P<id>\d+)', views.comment, name='comment'),
    url(r'^editprofile/', views.editprofile, name='editprofile'),
    url(r'^vote/$', views.like, name='like'),
    url(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
