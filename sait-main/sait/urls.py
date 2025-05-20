
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import ind1_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('ind1.html', ind1_view, name='ind1'),
    path('', include('counter.urls')),
]
