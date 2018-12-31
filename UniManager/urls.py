"""UniManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views

# Routes starting with "/"
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search-user/', views.search_user, name='search-user'),
    path('search-title/', views.search_title, name='search-title'),
    path('search-content/', views.search_content, name='search-content'),
    path('search-category/', views.search_category, name='search-category'),
    path('exams/', views.exams, name='exams'),
    path('exam/edit/<int:id>', views.edit_exam, name='edit_exam'),
    path('exam/delete/<int:id>', views.delete_exam, name='delete_exam'),
    path('profile/', views.profile, name='profile'),
    path('post/create', views.create_post, name='create_post'),
    path('post/edit/<int:id>', views.edit_post, name='edit_post'),
    path('post/delete/<int:id>', views.delete_post, name='delete_post'),
    path('post/display/', views.display_posts, name='display_post'),
    path('post/get/<int:id>', views.get_post, name='get_post'),
    path('post/comment/<int:id>', views.comment_post, name='comment_post'),
    path('profile/info/<str:username>', views.profile_info, name='profile_info' ),
    path('profile/posts/<str:username>', views.profile_posts, name='profile_posts' ),
    path('comment/delete/<int:id>', views.delete_comment, name='delete_comment'),

    # Routing per accounts/
    path('accounts/', include('app.urls')),

    path('admin/', admin.site.urls, name='admin'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
