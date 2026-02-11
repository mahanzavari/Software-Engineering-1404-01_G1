from django.contrib import admin
from .models import Question, Evaluation, DetailedScore, APILog

class DetailedScoreInline(admin.TabularInline):
    model = DetailedScore
    extra = 0
    readonly_fields = ('criterion', 'score_value', 'comment')
    can_delete = False

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'task_type', 'mode', 'difficulty', 'question_id')
    list_filter = ('task_type', 'mode', 'difficulty')
    search_fields = ('title', 'prompt_text')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'task_type', 'mode', 'difficulty')
        }),
        ('Content', {
            'fields': ('prompt_text', 'reading_text', 'resource_url')
        }),
        ('System ID', {
            'fields': ('question_id',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('question_id',)

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('evaluation_id', 'user_id', 'task_type', 'overall_score', 'created_at')
    list_filter = ('task_type', 'created_at')
    search_fields = ('user_id', 'evaluation_id')
    readonly_fields = ('evaluation_id', 'user_id', 'question', 'created_at', 'rubric_version_id', 'overall_score', 'ai_feedback', 'transcript_text')
    inlines = [DetailedScoreInline]

    fieldsets = (
        ('Evaluation Info', {
            'fields': ('evaluation_id', 'user_id', 'question', 'task_type')
        }),
        ('Submission Data', {
            'fields': ('submitted_text', 'audio_path', 'transcript_text')
        }),
        ('Scoring Results', {
            'fields': ('overall_score', 'ai_feedback')
        }),
        ('Meta', {
            'fields': ('created_at', 'rubric_version_id')
        }),
    )

    def has_add_permission(self, request):
        return False

@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'endpoint', 'method', 'status_code', 'latency_ms', 'timestamp')
    list_filter = ('method', 'status_code', 'timestamp')
    search_fields = ('endpoint', 'user_id')
    readonly_fields = [field.name for field in APILog._meta.fields]

    def has_add_permission(self, request):
        return False
        
    def has_change_permission(self, request, obj=None):
        return False