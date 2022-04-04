from django.contrib import admin
from .models import Question, Comment


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Админка вопроса"""

    list_display = ("id", "title", "category", "answer", "public")
    list_filter = ("public", "category")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка комментария"""

    list_display = ("id", "body", "question", "owner")
