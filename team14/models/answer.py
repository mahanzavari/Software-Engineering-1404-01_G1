from django.db import models
from django.contrib.auth import get_user_model
from .question import Question


User = get_user_model()

class UserSession(models.Model):
    MODE_CHOICES = [
        ('exam', 'Exam Mode'),
        ('practice', 'Practice Mode'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    total_score = models.IntegerField(null=True, blank=True)
    scaled_score = models.FloatField(null=True, blank=True)
    exam_version = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user} - {self.mode}"


class UserAnswer(models.Model):
    session = models.ForeignKey(
        UserSession,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    selected_option = models.ForeignKey(
        'Option',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_correct = models.BooleanField()
    response_time = models.FloatField(help_text="Time in seconds")
    changed_count = models.IntegerField(default=0)