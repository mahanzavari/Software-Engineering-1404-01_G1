import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class TaskType(models.TextChoices):
    WRITING = 'writing', _('Writing')
    SPEAKING = 'speaking', _('Speaking')

class Mode(models.TextChoices):
    INDEPENDENT = 'independent', _('Independent')
    INTEGRATED = 'integrated', _('Integrated')

class Question(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, default="New Question") 
    prompt_text = models.TextField()
    reading_text = models.TextField(blank=True, null=True)
    task_type = models.CharField(max_length=20, choices=TaskType.choices, default=TaskType.WRITING)
    mode = models.CharField(max_length=20, choices=Mode.choices, default=Mode.INDEPENDENT)
    resource_url = models.CharField(max_length=500, blank=True, null=True)
    difficulty = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.get_task_type_display()} - {self.title}"

class Evaluation(models.Model):
    evaluation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='evaluations')
    task_type = models.CharField(max_length=20, choices=TaskType.choices, default=TaskType.WRITING)
    submitted_text = models.TextField(blank=True, null=True)
    audio_path = models.CharField(max_length=500, blank=True, null=True)
    overall_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    ai_feedback = models.TextField(blank=True, null=True)
    transcript_text = models.TextField(blank=True, null=True)
    rubric_version_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user_id', '-created_at'])]

    def __str__(self):
        return f"Eval {self.evaluation_id} - Score: {self.overall_score}"

class DetailedScore(models.Model):
    score_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='detailed_scores')
    criterion = models.CharField(max_length=50)
    score_value = models.DecimalField(max_digits=3, decimal_places=1)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.criterion}: {self.score_value}"

class APILog(models.Model):
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(null=True, blank=True)
    endpoint = models.CharField(max_length=200)
    method = models.CharField(max_length=10, default='GET')
    status_code = models.IntegerField()
    latency_ms = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    error_message = models.TextField(blank=True, null=True)
    request_size = models.IntegerField(null=True, blank=True)
    response_size = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['endpoint', '-timestamp']),
            models.Index(fields=['status_code', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.method} {self.endpoint} - {self.status_code}"