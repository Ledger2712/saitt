from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='index.html',
        extra_context={'form_type': 'login'}
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
