import os
import google.generativeai as genai
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from django.shortcuts import render, redirect
from django.views import View

from .models import Story
from .serializers import StorySerializer

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


class StoryCreateView(CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = StorySerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data["title"]

        prompt_template = (
            f"Once upon a time, there was a story about '{title}'. "
            "This story is about an adventure where the main character faces various challenges. "
            "The story will unfold based on the decisions the reader makes. "
            "The introduction should set the scene for the story, and the next passage should follow the choices made by the user."
            "The story should be simple enough for instructional-level readers to understand."
        )


        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

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

        model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

        response = model.generate_content(title)
        generated_response = response.text.strip()

        if isinstance(response, str):
            return Response(
                {
                "status": "error",
                "prompt": generated_response,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
            "status": "success",
            "response": generated_response,
            },
            status=status.HTTP_201_CREATED,
        )

        

