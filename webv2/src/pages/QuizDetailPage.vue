<template>
  <div class="min-h-screen bg-gradient-to-b from-pink-50 to-indigo-50 flex">
    <AppSidebar />
    <div 
      class="flex-1 transition-all duration-300" 
      :class="[isSidebarOpen ? 'ml-64' : 'ml-20']"
    >
      <div class="p-6 max-w-4xl mx-auto">
        <div v-if="loading" class="flex justify-center items-center h-64">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-indigo-500 border-t-transparent"></div>
          <p class="ml-2 text-indigo-600">Loading quiz details...</p>
        </div>
        
        <div v-else-if="error" class="bg-red-100 text-red-700 p-4 rounded-xl mb-6 border-2 border-red-200">
          {{ error }}
        </div>
        
        <div v-else class="bg-white rounded-3xl shadow-lg border-2 border-indigo-100 overflow-hidden relative">
          <div class="absolute -top-10 -right-10 w-24 h-24 bg-yellow-200 rounded-full opacity-30"></div>
          <div class="absolute -bottom-10 -left-10 w-28 h-28 bg-blue-200 rounded-full opacity-30"></div>
          
          <div class="p-6 border-b-2 border-indigo-100 bg-gradient-to-r from-purple-50 to-indigo-50 relative">
            <div class="flex justify-between items-center">
              <h2 class="text-2xl font-bold text-indigo-800 flex items-center">
                <span class="mr-3">📚</span> {{ quizDetail.story.title }} - Quiz Overview
              </h2>
              <div>
                <router-link 
                  to="/dashboard" 
                  class="px-5 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-full hover:from-indigo-700 hover:to-purple-700 transition-all shadow-md hover:shadow-lg transform hover:scale-105"
                >
                  Back to Dashboard
                </router-link>
              </div>
            </div>
          </div>
          
          <div class="p-6 bg-gradient-to-r from-indigo-50 to-purple-50 border-b-2 border-indigo-100">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="bg-white rounded-xl shadow-sm p-6 border-2 border-indigo-100">
                <div class="flex items-center">
                  <div class="p-3 rounded-full bg-blue-100 text-blue-600">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div class="ml-4">
                    <h2 class="text-lg font-semibold text-indigo-700">Questions</h2>
                    <p class="text-xl font-bold text-indigo-800">{{ quizDetail.quiz.total_questions }}</p>
                  </div>
                </div>
              </div>
              
              <div class="bg-white rounded-xl shadow-sm p-6 border-2 border-indigo-100">
                <div class="flex items-center">
                  <div class="p-3 rounded-full bg-green-100 text-green-600">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div class="ml-4">
                    <h2 class="text-lg font-semibold text-indigo-700">Score</h2>
                    <p class="text-xl font-bold text-indigo-800">{{ quizDetail.quiz.score }}%</p>
                  </div>
                </div>
              </div>
              
              <div class="bg-white rounded-xl shadow-sm p-6 border-2 border-indigo-100">
                <div class="flex items-center">
                  <div class="p-3 rounded-full bg-purple-100 text-purple-600">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div class="ml-4">
                    <h2 class="text-lg font-semibold text-indigo-700">Status</h2>
                    <p class="text-lg font-bold text-indigo-800">{{ quizDetail.quiz.is_complete ? 'Completed' : 'In Progress' }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="p-8 relative z-10 border-b-2 border-indigo-100">
            <h3 class="text-xl font-bold text-indigo-800 mb-4 flex items-center">
              <span class="mr-3">✨</span> About This Quiz
            </h3>
            <div class="bg-indigo-50 p-6 rounded-xl border-2 border-indigo-100 whitespace-pre-line">
              <p>This quiz tests your comprehension of the story "{{ quizDetail.story.title }}". It features {{ quizDetail.quiz.total_questions }} multiple-choice questions designed to assess your understanding of the main themes, characters, events, and details from the story.</p>
              
              <h4 class="font-semibold mt-4 mb-2 text-indigo-700">Learning Objectives:</h4>
              <ul class="space-y-2 text-indigo-700">
                <li class="flex items-start">
                  <span class="mr-2 mt-1">🔍</span>
                  <span>Recall key events and details from the story</span>
                </li>
                <li class="flex items-start">
                  <span class="mr-2 mt-1">🧠</span>
                  <span>Understand character motivations and development</span>
                </li>
                <li class="flex items-start">
                  <span class="mr-2 mt-1">🌟</span>
                  <span>Identify main themes and messages</span>
                </li>
                <li class="flex items-start">
                  <span class="mr-2 mt-1">🤔</span>
                  <span>Apply critical thinking to analyze the narrative</span>
                </li>
              </ul>
              
              <h4 class="font-semibold mt-4 mb-2 text-indigo-700">Tips for Success:</h4>
              <ul class="space-y-2 text-indigo-700">
                <li class="flex items-start">
                  <span class="mr-2 mt-1">📖</span>
                  <span>Read each question carefully</span>
                </li>
                <li class="flex items-start">
                  <span class="mr-2 mt-1">🧩</span>
                  <span>Consider all options before selecting your answer</span>
                </li>
                <li class="flex items-start">
                  <span class="mr-2 mt-1">📝</span>
                  <span>Use the feedback provided after each question to improve understanding</span>
                </li>
              </ul>
            </div>
          </div>
          
          <div v-if="quizDetail.previous_attempts && quizDetail.previous_attempts.length > 0" class="p-8 border-b-2 border-indigo-100">
            <h3 class="text-xl font-bold text-indigo-800 mb-4 flex items-center">
              <span class="mr-3">📊</span> Previous Attempts
            </h3>
            <div class="overflow-x-auto bg-indigo-50 p-4 rounded-xl border-2 border-indigo-100">
              <table class="min-w-full divide-y divide-indigo-200">
                <thead class="bg-indigo-100">
                  <tr>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-indigo-700 uppercase tracking-wider">Attempt</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-indigo-700 uppercase tracking-wider">Date</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-indigo-700 uppercase tracking-wider">Score</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-indigo-700 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-indigo-100">
                  <tr v-for="(attempt, index) in quizDetail.previous_attempts" :key="index">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm font-medium text-indigo-700">{{ index + 1 }}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm text-indigo-600">{{ formatDate(attempt.date) }}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm text-indigo-700">{{ attempt.score }}%</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button 
                        class="px-4 py-2 bg-indigo-100 text-indigo-700 rounded-full hover:bg-indigo-200 transition-all"
                        @click="viewAttemptDetails(attempt.id)"
                      >
                        View Details
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <div class="p-8">
            <div class="flex justify-between">
              <button 
                class="px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-lg font-bold rounded-full hover:from-indigo-700 hover:to-purple-700 transition-all shadow-md hover:shadow-lg transform hover:scale-105"
                @click="startNewQuiz"
              >
                Take Quiz Again
              </button>
              
              <button 
                class="px-8 py-4 bg-gradient-to-r from-purple-100 to-indigo-100 text-indigo-700 text-lg font-bold rounded-full hover:from-purple-200 hover:to-indigo-200 transition-all shadow-md hover:shadow-lg transform hover:scale-105"
                @click="reviewStory"
              >
                Review Story
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppSidebar from '@/components/AppSidebar.vue';
import { inject, ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/utils/auth-interceptor';

export default {
  name: 'QuizDetailView',
  components: {
    AppSidebar
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const storyId = route.params.id;
    const quizDetail = ref(null);
    const loading = ref(true);
    const error = ref(null);
    const isSidebarOpen = inject('sidebarState', ref(true));

    const fetchQuizDetails = async () => {
      loading.value = true;
      error.value = null;
      
      try {
        const response = await api.get(`http://127.0.0.1:8000/api/v1/storybook/story/${storyId}/quiz/`, {
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`
          }
        });
        
        quizDetail.value = response.data;
      } catch (err) {
        console.error('Error fetching quiz details:', err);
        if (err.response && err.response.data) {
          error.value = err.response.data.detail || 'Failed to load quiz details.';
        } else {
          error.value = 'An error occurred while loading quiz details.';
        }
      } finally {
        loading.value = false;
      }
    };

    const formatDate = (dateString) => {
      if (!dateString) return '';
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    };
    
    const startNewQuiz = () => {
      router.push(`/quiz/${storyId}/`);
    };
    
    const reviewStory = () => {
      router.push(`/story/${storyId}`);
    };
    
    const viewAttemptDetails = (attemptId) => {
      router.push(`/quiz/${storyId}/attempt/${attemptId}`);
    };
    
    onMounted(() => {
      fetchQuizDetails();
    });
    
    return {
      quizDetail,
      loading,
      error,
      isSidebarOpen,
      formatDate,
      startNewQuiz,
      reviewStory,
      viewAttemptDetails
    };
  }
};
</script>