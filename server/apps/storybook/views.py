import os
import re
import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.core.validators import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Story, Quiz
from django.contrib.auth import authenticate, login
import google.generativeai as genai
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
logger = logging.getLogger(__name__)

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def is_valid_text(text):
    """
    Returns True if the text is at least 3 characters long
    and contains at least one vowel (a, e, i, o, u), otherwise False.
    This is a simple heuristic to help filter out random inputs.
    """
    text = text.strip()
    if len(text) < 3:
        return False
    if not re.search(r'[aeiouAEIOU]', text):
        return False
    return True

@ensure_csrf_cookie
def get_csrf_token(request):
    """
    View to get CSRF token and set it as a cookie
    """
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})

class HomeView(View):
    """Landing page where users input the story topic."""
    def get(self, request):
        return render(request, 'storybook/home.html')

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    """Handles login form display and processing."""
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            username = request.POST.get('username')
            password = request.POST.get('password')
        
        print("Attempting login for:", username)
        
        user = authenticate(request, username=username, password=password)
        
        print("Authentication result:", user)
        
        if user is not None:
            login(request, user)
            print("User logged in:", request.user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)

class RegisterView(View):
    """Renders the registration page."""
    def get(self, request):
        return render(request, 'storybook/register.html')

class StoryCreateView(APIView):
    """Handles story generation and Gemini AI integration."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get('title', '').strip()
        difficulty_level = request.data.get('difficulty_level', 'beginner')
        if not title or not is_valid_text(title):
            return JsonResponse({"error": "Invalid story title."}, status=400)

        story = Story.objects.create(
            title=title,
            user=request.user,
            difficulty_level=difficulty_level,
            word_limit=150,
            voice_interaction=False,
            include_quiz=True,
            number_of_questions=20,
            question_type="short-answer"
        )

        try:
            prompt = f"Generate a short story introduction for the topic: {title}"
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            generated_text = response.text.strip()

            story.introduction = generated_text
            story.current_passage = generated_text
            story.save()

            return JsonResponse({
                "id": story.id,
                "title": story.title,
                "introduction": story.introduction,
                "current_passage": story.current_passage,
                "difficulty_level": story.difficulty_level,
            }, status=201)

        except Exception as e:
            story.delete()
            return JsonResponse({"error": str(e)}, status=500)
        
class StoryAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        stories = Story.objects.filter(user=request.user).order_by('-generated_on')
        
        stories_data = []
        for story in stories:
            has_quiz = story.quizzes.exists()
            quiz_complete = False
            if has_quiz:
                quiz = story.quizzes.first()
                quiz_complete = quiz.current_question >= quiz.total_questions
            
            stories_data.append({
                'id': story.id,
                'title': story.title,
                'introduction': story.introduction,
                'complete_story': bool(story.complete_story),
                'continuation_count': story.continuation_count,
                'generated_on': story.generated_on.isoformat(),
                'has_quiz': has_quiz,
                'quiz_complete': quiz_complete
            })
        
        return Response(stories_data)
    
    def post(self, request):
        title = request.data.get('title')
        if not title:
            return Response({'error': 'Title is required'}, status=400)
        
        story = Story.objects.create(
            title=title,
            user=request.user,
            difficulty_level='beginner',
            word_limit=150,
            voice_interaction=False,
            include_quiz=True,
            number_of_questions=20,
            question_type="short-answer"
        )
        
        return Response({
            'id': story.id,
            'title': story.title,
            'introduction': story.introduction,
            'complete_story': bool(story.complete_story),
            'continuation_count': story.continuation_count,
            'generated_on': story.generated_on.isoformat()
        })

class StoryView(APIView):
    """Handles story continuation and quiz generation."""
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, story_id):
        if not request.user.is_authenticated:
            return Response({
                'error': 'Authentication required',
                'detail': 'You need to be logged in to view this story',
                'story_id': story_id
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            story = get_object_or_404(Story, id=story_id, user=request.user)
            
            return Response({
                'id': story.id,
                'title': story.title,
                'introduction': story.introduction,
                'current_passage': story.current_passage,
                'complete_story': story.complete_story,
                'continuation_count': story.continuation_count,
                'steps_remaining': max(3 - story.continuation_count, 0)
            })
            
        except Exception as e:
            return Response({
                'error': 'Story not found',
                'detail': str(e)
            }, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, story_id):
        if not request.user.is_authenticated:
            return Response({
                'error': 'Authentication required',
                'detail': 'You need to be logged in to continue this story'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            story = get_object_or_404(Story, id=story_id, user=request.user)
            user_prompt = request.data.get('prompt', '').strip()

            if story.continuation_count >= 3:
                return Response({
                    'error': 'Story complete',
                    'detail': 'This story has already concluded.'
                }, status=status.HTTP_400_BAD_REQUEST)

            if not user_prompt or not is_valid_text(user_prompt):
                return Response({
                    'error': 'Invalid prompt',
                    'detail': 'Please enter a valid continuation prompt.'
                }, status=status.HTTP_400_BAD_REQUEST)

            prompt = f"""Continue this educational story for Philippine Grade 4-5 students.
            Previous story: {story.complete_story or story.introduction}
            Reader's choice: {user_prompt}
            
            Requirements:
            1. Use simple English (Grade 4-5 level)
            2. Maximum 65 words
            3. Include character dialogue
            4. {"CONCLUDE THE STORY WITH A MORAL LESSON" if story.continuation_count >= 2 else "End with a new decision point"}
            5. Incorporate dialogue-based storytelling
            6. Format: Single paragraph with proper punctuation

            Please ensure the content aligns with the Philippine Informal Reading Inventory (Phil-IRI) standards for Grade 5 instructional-level readers.
            """

            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
            ]

            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            new_passage = self.clean_response(response.text)
            safety_settings=safety_settings

            story.continuation_count += 1
            story.user_responses += f"\nUser choice: {user_prompt}"
            story.current_passage = new_passage
            
            is_ending = self.is_ending(new_passage)
            if story.continuation_count >= 3 or is_ending:
                story.complete_story = f"{story.complete_story}\n{new_passage}" if story.complete_story else new_passage
                story.current_passage = ""
                story.save()
                
                return Response({
                    'status': 'complete',
                    'message': 'Story has concluded. A quiz is now available.',
                    'story_id': story.id,
                    'redirect_to_quiz': True
                })
            
            story.save()
            
            return Response({
                'status': 'continued',
                'message': 'Story continued successfully',
                'current_passage': new_passage,
                'continuation_count': story.continuation_count,
                'steps_remaining': max(3 - story.continuation_count, 0)
            })

        except Exception as e:
            return Response({
                'error': 'Error continuing story',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def clean_response(self, text):
        """Clean and format the AI response"""
        cleaned = re.sub(r'\*\*|\[.*?\]', '', text)

    def is_ending(self, text):
        """Detect story conclusion in generated text"""
        return any(keyword in text.lower() for keyword in ['moral'])

class QuizAPIView(APIView):
    """API endpoint for quiz data"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, story_id):
        story = get_object_or_404(Story, id=story_id, user=request.user)
        
        try:
            if not story.quizzes.exists():
                try:
                    self.generate_quiz(story)
                except Exception as e:
                    return Response({"error": f"Failed to generate quiz: {str(e)}"}, status=500)
                story.refresh_from_db()

            quiz = story.quizzes.first()

            logger.debug("Story: %s", story)
            logger.debug("Quiz: %s", quiz)

            return Response({
                "story": {
                    "id": story.id,
                    "title": story.title
                },
                "quiz": {
                    "id": quiz.id,
                    "score": quiz.score,
                    "total_questions": quiz.total_questions,
                    "current_question": quiz.current_question,
                    "is_complete": quiz.current_question >= quiz.total_questions,
                    "questions": quiz.questions 
                }
            }, status=200)

        except Exception as e:
            logger.error("Error fetching quiz data: %s", str(e))
            return Response({"error": f"Quiz error: {str(e)}"}, status=500)

    def post(self, request, story_id):
        try:
            story = get_object_or_404(Story, id=story_id, user=request.user)
            quiz = get_object_or_404(Quiz, story_id=story_id)
            user_answers = request.data.get("answers", [])
            
            if not isinstance(user_answers, list):
                return Response({"error": "Invalid answers format."}, status=status.HTTP_400_BAD_REQUEST)
            
            quiz.user_answers = {} if not quiz.user_answers else dict(quiz.user_answers)
            score = 0
            
            for i, user_answer in enumerate(user_answers):
                question_key = f'q{i + 1}'
                
                if question_key in quiz.questions:
                    correct_letter = quiz.questions[question_key]['answer']
                    
                    user_letter = None
                    if user_answer is not None:
                        if isinstance(user_answer, int):
                            user_letter = chr(65 + user_answer)  
                        else:
                            user_letter = user_answer
                    
                    is_correct = user_letter == correct_letter
                    
                    # Store the answer
                    quiz.user_answers[question_key] = {
                        "user_answer": user_letter,
                        "correct": is_correct
                    }
                    
                    if is_correct:
                        score += 1
                
            quiz.score = score
            quiz.current_question = quiz.total_questions 
            quiz.save()
            
            return Response({
                "message": "Quiz submitted successfully!",
                "score": quiz.score,
                "total_questions": quiz.total_questions,
                "user_answers": quiz.user_answers
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error("Failed to save quiz: %s", str(e))
            return Response({"error": f"Failed to save quiz results: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def generate_quiz(self, story):
        """Generate multiple-choice quiz based solely on story content"""
        try:
            prompt = f"""Generate 20 multiple-choice questions solely for this story:
            {story.complete_story}
            
            STRICT REQUIREMENTS:
            1. Questions in English appropriate for Grade 4-5 students.
            2. Each question must be strictly directly based on the story and must not reference unrelated content.
            3. Strictly do NOT include any meta-information or questions about how the questions are created or their types.
            4. Format as JSON:
            {{
                "q1": {{
                    "question": "...",
                    "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
                    "answer": "A"  // Correct option letter
                }},
                ...
                "q20": {{
                    "question": "...",
                    "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
                    "answer": "B"
                }}
            }}
            5. Vary the question types by using the following Levels of Questions: Literal, Inferential, and Evaluative. 
            6. Use Bloom's Taxonomy levels (Knowledge, Comprehension, Application, Analysis, Evaluation) applicable for Grade 4-5 students.
            7. Ensure only one correct answer per question.
            8. Use simple language appropriate for Grade 4-5 level.
            """
            
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            questions = json.loads(response.text.replace('```json', '').replace('```', ''))
            
            Quiz.objects.create(
                story=story,
                questions=questions,
                total_questions=20
            )

        except Exception as e:
            logger.error("Quiz creation failed: %s", str(e))
            raise Exception(f"Quiz creation failed: {str(e)}")
        
class DashboardView(LoginRequiredMixin, View):
    """Display the logged-in user's dashboard with a list of their generated stories."""
    def get(self, request):
        user = request.user
        stories = Story.objects.filter(user=user).order_by('-generated_on')
        context = {
            'user': user,
            'stories': stories,
        }
        return render(request, 'storybook/dashboard.html', context)

class StoryDetailView(APIView):
    """Display the full details of a story."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, story_id):
        try:
            story = get_object_or_404(Story, id=story_id, user=request.user)
            return Response({
                'id': story.id,
                'title': story.title,
                'introduction': story.introduction,
                'complete_story': story.complete_story,
                'user_responses': story.user_responses,
                'difficulty_level': story.difficulty_level,
                'generated_on': story.generated_on,
                'has_quiz': story.quizzes.exists()
            })
        except Exception as e:
            return Response({'error': 'Story not found', 'detail': str(e)}, status=404)
    def delete(self, request, story_id):
        try:
            story = get_object_or_404(Story, id=story_id, user=request.user)
            story.delete()
            return Response({'message': 'Story deleted successfully.'}, status=204)
        except Exception as e:
            return Response({'error': 'Failed to delete story', 'detail': str(e)}, status=500)
        
class QuizDetailView(APIView):
    """Display the details of a quiz for a story and handle quiz submissions."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, story_id):
        story = get_object_or_404(Story, id=story_id, user=request.user)
        quiz = story.quizzes.first()
        
        if not quiz:
            return Response(
                {"detail": "No quiz available for this story."}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        if not quiz.is_complete:
            return Response(
                {"detail": "Quiz is still in progress. Please complete it before viewing details."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        response_data = {
            "story": {
                "id": story.id,
                "title": story.title,
            },
            "quiz": {
                "id": quiz.id,
                "total_questions": quiz.total_questions,
                "score": quiz.score,
                "is_complete": quiz.is_complete,
                "questions": quiz.questions, 
                "user_answers": quiz.user_answers 
            }
        }
        
        return Response(response_data)