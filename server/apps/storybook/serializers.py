from rest_framework import serializers

# Models
from .models import Story

class StorySerializer(serializers.ModelSerializer):


    class Meta:
        model = Story
        fields = [
            'title',
            'difficulty_level',
            'word_limit',
            'voice_interaction',
            'include_quiz',
            'number_of_questions',
            'introduction',
            'current_passage',
            'user_responses',
            'complete_story',
            'generated_on',
        ]
        read_only_fields = ['generated_on', 'introduction', 'current_passage', 'complete_story', 'user_responses']



