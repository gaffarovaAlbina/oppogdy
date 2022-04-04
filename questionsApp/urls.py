from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("users", views.QuestionList.as_view()),
    path("user", views.QuestionList.as_view()),
    path("questions", views.QuestionList.as_view()),
    path("question/<int:pk>", views.QuestionDetail.as_view()),
    path("question/new", views.QuestionAdd.as_view()),
    path("questions/public", views.PublicQuestionList.as_view()),
    path("user/questions", views.UserQuestionList.as_view()),
    path("comments", views.CommentList.as_view()),
    path("comment/<int:pk>", views.CommentDetail.as_view()),
    path("question/<int:pk>/answer", views.AnswerQuestionDetail.as_view()),
    path("question/<int:pk>/edit", views.UpdateQuestionDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)


# развернуть маленький сервер, закинуть
