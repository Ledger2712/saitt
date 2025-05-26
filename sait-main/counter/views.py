# counter/views.py
from django.shortcuts import render
from django.http import StreamingHttpResponse
from .utils import gen_frames

def index(request):
    return render(request, 'index.html')

def video_feed(request):
    return StreamingHttpResponse(
        gen_frames(0),   # или 0 для веб-камеры
        content_type='multipart/x-mixed-replace; boundary=frame'
    )
