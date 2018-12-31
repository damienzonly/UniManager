from django.urls import path
from . import views as app_views


# Routes starting with "/accounts"
urlpatterns = [
    path('signup/', app_views.signup, name='signup'),
    path('login/', app_views.login, name='login'),
    path('logout/', app_views.logout, name='logout'),
]
