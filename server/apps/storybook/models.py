from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Story(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    #user_id = models.UUIDField(blank=True, null=True)

    # AI Storybook Details Prompts
    #prompt = models.TextField(blank=False, null=True)
    #message = models.TextField(blank=False, null=True)

    # Timestamps
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)


    # Story Details
    title = models.CharField(max_length=255, help_text="The topic or title of the story.")
    difficulty_level = models.CharField(
        max_length=50,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ]
    )
    word_limit = models.PositiveIntegerField(default=250)

    # User Interaction Details
    user = models.ForeignKey(User, on_delete=models.CASCADE)#, null=True, blank=True)
    voice_interaction = models.BooleanField(default=True)

    # Quiz Configuration
    include_quiz = models.BooleanField(default=True, help_text="Whether a quiz should follow the story.")
    number_of_questions = models.PositiveIntegerField(default=20)
    question_type = models.CharField(
        max_length=50, 
        default="short-answer"
    )

    # Dynamic Story Generation
    introduction = models.TextField(blank=True)
    current_passage = models.TextField(blank=True)
    user_responses = models.TextField(
        blank=True,
        help_text="Stores the user's responses or decisions as a JSON string."
    )
    complete_story = models.TextField(blank=True, help_text="The entire generated story.")

    # Metadata
    generated_on = models.DateTimeField(auto_now_add=True)

    # Track user continuation
    continuation_count = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        #return self.id
        return f"{self.title} by {self.user.username}"
        
    def get_quiz(self):
        return self.quizzes.first()

    class Meta:
        db_table = "stories"
        ordering = ["-generated_on"]
        verbose_name = "Story"
        verbose_name_plural = "Stories"

    
class Quiz(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='quizzes')
    questions = models.JSONField(help_text="Stores questions with options and correct answers in JSON format.")  # Stores questions and answers 
    generated_on = models.DateTimeField(auto_now_add=True)
    current_question = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=20)  # Add this line
    user_answers = models.JSONField(blank=True, null=True, help_text="Stores user's answers and their correctness per question.")

    def __str__(self):
        return f"Quiz for {self.story.title}"

    @property
    def is_complete(self):
        return self.current_question >= self.total_questions

    class Meta:
        verbose_name_plural = "Quizzes"
