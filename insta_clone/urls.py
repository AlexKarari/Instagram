from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$', views.timeline, name='various'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^userprofile/(\d+)', views.user_profile, name='user_profile'),
    url(r'^newphoto/', views.new_photo, name='new_photo'),
    url(r'^comment/(?P<id>\d+)', views.comment, name='comment'),
    url(r'^editprofile/', views.editprofile, name='editprofile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
