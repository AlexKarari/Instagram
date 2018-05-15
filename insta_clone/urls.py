from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$', views.timeline, name='various'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^userprofile/(\d+)', views.other_profile, name='other_profiles'),
    url(r'^myprofile/', views.my_profile, name='myprofile'),
    url(r'^newphoto/', views.new_photo, name='new_photo'),
    url(r'^comment/(?P<id>\d+)', views.comment, name='comment'),
    url(r'^editprofile/', views.editprofile, name='editprofile'),
    url(r'^vote/$', views.like, name='like'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
