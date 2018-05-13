from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$', views.timeline, name='various'),
    url(r'^profile/(\d+)', views.profile, name="profile"),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^user/(\d+)', views.userProfile, name='userProfiles'),
    url(r'^image/(\d+)', views.soloImage, name='soloImage'),
    url(r'^new/comment$', views.new_comment, name='new_comment'),
    url(r'^new/status/$', views.new_status, name='newStatus'),


    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
