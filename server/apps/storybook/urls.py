from django.urls import path
from .views import (
    HomeView, LoginView, RegisterView, StoryCreateView, StoryView, \
    DashboardView, StoryDetailView, QuizDetailView, get_csrf_token,
    StoryAPIView, QuizAPIView
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path("create/", StoryCreateView.as_view(), name="create-story"),
    path("story/<int:story_id>/", StoryView.as_view(), name="story"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('csrf/', get_csrf_token, name='csrf'),
    path('story/<int:story_id>/detail/', StoryDetailView.as_view(), name='story_detail'),
    path('story/<int:story_id>/quiz/', QuizDetailView.as_view(), name='quiz_detail'),

    # New Endpoints
    path('api/stories/', StoryAPIView.as_view(), name='story_api'),
    path('quiz/<int:story_id>/', QuizAPIView.as_view(), name='quiz'),
]

