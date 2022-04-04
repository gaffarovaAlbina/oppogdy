from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import login, logout

urlpatterns = [
    path("users", views.UserList.as_view()),
    path("user", views.UserDetail.as_view()),
    path("login", login),
    path("logout", logout),
]
