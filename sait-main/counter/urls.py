from django.urls import path
from .views import index, video_feed

urlpatterns = [
    path('',      index,      name='counter-index'),
    path('feed/', video_feed, name='video-stream'),
]