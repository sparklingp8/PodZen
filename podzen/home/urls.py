from django.urls import path
from .views import home_view, get_video_link

urlpatterns = [
    path('', home_view, name='home'),
    path('video-link', get_video_link, name='video_link'),
]
