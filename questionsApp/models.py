from django.db import models


class Question(models.Model):
    """Модель вопроса"""

    HEALTH = "Здоровье"
    STUDY = "Обучение"
    FINANCE = "Финансы"
    DOCUMENTS = "Документы"
    OTHER = "Другое"
    CATEGORIES = (
        (HEALTH, "Здоровье"),
        (STUDY, "Обучение"),
        (FINANCE, "Финансы"),
        (DOCUMENTS, "Документы"),
        (OTHER, "Другое"),
    )

    title = models.CharField(max_length=500)
    createdQuestion = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        "auth.User",
        related_name="questions",
        on_delete=models.SET_NULL,
        null=True,
    )
    public = models.BooleanField(default=False)
    answer = models.TextField(null=True, blank=True)
    createdAnswer = models.DateTimeField(null=True, blank=True)
    category = models.CharField(
        max_length=300, choices=CATEGORIES, null=True, blank=True
    )

    class Meta:
        ordering = ["createdQuestion"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель комментария"""

    body = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        "auth.User", related_name="comments", on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        "Question", related_name="comments", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["created"]
