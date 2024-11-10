"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.user_login, name="login"),  # Set login as the landing page
    path("register/", views.register, name="register"),
    path("landing/", views.landing_page, name="landing_page"),  # Landing page route
    path('preferences/', views.preferences_page, name='preferences_page'),
    path('submit_preferences/', views.submit_preferences, name='submit_preferences'),
    path('start_swiping/', views.start_swiping, name='start_swiping'),
    path('swipe_papers/', views.swipe_papers, name='swipe_papers'), 
    path('paper-swipe/', views.paper_swipe_view, name='paper_swipe'),
    path('api/get-next-paper/', views.get_next_paper, name='get_next_paper'),
    path('api/rate-paper/', views.rate_paper, name='rate_paper'),
    path("profile", views.profile_view, name="profile")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
