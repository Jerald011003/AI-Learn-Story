from django.contrib import admin

# Models
from .models import Story, Quiz

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "generated_on", "difficulty_level")
    readonly_fields = ("user", "generated_on", "voice_interaction", "question_type")
    fieldsets = (
        ("Story Details", {
            "fields": ("title", "difficulty_level", "word_limit"),
        }),
        ("User Interaction", {
            "fields": ("user", "voice_interaction"),
        }),
        ("Quiz Configuration", {
            "fields": ("include_quiz", "number_of_questions", "question_type"),
        }),
        ("Content", {
            "fields": ("introduction", "current_passage", "complete_story", "user_responses"),
        }),
        ("Metadata", {
            "fields": ("generated_on", "continuation_count"),
        }),
    )
    list_filter = ("difficulty_level", "generated_on", "user")
    search_fields = ("title", "user__username")

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'story', 'generated_on']
    list_filter = ('generated_on',)
    search_fields = ('story__title',)