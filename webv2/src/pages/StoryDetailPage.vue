<template>
  <div class="min-h-screen bg-gradient-to-b from-pink-50 to-indigo-50 flex">
    <AppSidebar />
    <div class="flex-1 transition-all duration-300" :class="[isSidebarOpen ? 'ml-64' : 'ml-20']">
      <div class="p-6 max-w-4xl mx-auto">
        <div v-if="loading" class="flex justify-center items-center h-64">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-indigo-500 border-t-transparent"></div>
          <p class="ml-2 text-indigo-600 font-medium">Loading story details...</p>
        </div>
        
        <div v-else-if="error" class="bg-red-100 text-red-700 p-4 rounded-xl shadow-md mb-6 border-2 border-red-200">
          {{ error }}
        </div>
        
        <div v-else class="bg-white rounded-3xl shadow-lg border-2 border-indigo-100 overflow-hidden relative">
          <div class="absolute -top-10 -right-10 w-24 h-24 bg-yellow-200 rounded-full opacity-30"></div>
          <div class="absolute -bottom-10 -left-10 w-28 h-28 bg-blue-200 rounded-full opacity-30"></div>
          
          <div class="p-6 border-b-2 border-indigo-100 bg-gradient-to-r from-purple-50 to-indigo-50 relative">
            <div class="flex justify-between items-center">
              <h2 class="text-2xl font-bold text-indigo-800 flex items-center">
                <span class="mr-3">📚</span> Story Details
              </h2>
              <router-link 
                to="/dashboard" 
                class="px-5 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold rounded-full hover:from-indigo-700 hover:to-purple-700 transition-all shadow-md hover:shadow-lg transform hover:scale-105"
              >
                Back to Dashboard
              </router-link>
            </div>
          </div>
          
          <div class="p-8 relative z-10">
            <h3 class="text-xl font-bold text-indigo-800 mb-6 flex items-center">
              <span class="mr-2">📖</span> {{ story.title }}
            </h3>
            
            <div class="mb-8">
              <p class="text-md font-bold text-indigo-700 mb-2 flex items-center">
                <span class="mr-2"></span> Difficulty Level:
              </p>
              <p class="bg-gradient-to-r from-blue-100 to-indigo-100 text-indigo-800 px-4 py-2 rounded-full text-md inline-block font-bold border-2 border-indigo-200 shadow-sm">
                {{ story.difficulty_level || 'Beginner' }}
              </p>
            </div>
            
            <div class="space-y-8">
              <div>
                <h4 class="text-lg font-bold text-indigo-800 mb-4 flex items-center">
                  <span class="mr-2">🌟</span> Content
                </h4>
                
                <div class="mb-6">
                  <p class="text-md font-bold text-indigo-700 mb-2 flex items-center">
                    <span class="mr-2"></span> Introduction:
                  </p>
                  <div class="bg-indigo-50 p-6 rounded-xl border-2 border-indigo-100 whitespace-pre-line shadow-inner text-indigo-800">
                    {{ story.introduction }}
                  </div>
                </div>
                
                <div class="mb-6">
                  <p class="text-md font-bold text-indigo-700 mb-2 flex items-center">
                    <span class="mr-2"></span> Complete Story:
                  </p>
                  <div class="bg-indigo-50 p-6 rounded-xl border-2 border-indigo-100 max-h-96 overflow-y-auto whitespace-pre-line shadow-inner text-indigo-800">
                    {{ story.complete_story }}
                  </div>
                </div>
                
                <div v-if="story.user_responses">
                  <p class="text-md font-bold text-indigo-700 mb-2 flex items-center">
                    <span class="mr-2"></span> Your Choices:
                  </p>
                  <div class="bg-indigo-50 p-6 rounded-xl border-2 border-indigo-100 whitespace-pre-line shadow-inner text-indigo-800">
                    {{ story.user_responses }}
                  </div>
                </div>
              </div>
              
              <div>
                <h4 class="text-lg font-bold text-indigo-800 mb-4 flex items-center">
                  <span class="mr-2">📋</span> Story Information
                </h4>
                <p class="bg-white p-4 rounded-xl border-2 border-indigo-100 text-indigo-700 shadow-sm">
                  <span class="font-bold">Created on:</span> {{ formatDate(story.generated_on) }}
                </p>
              </div>
            </div>
            
            <div v-if="story.has_quiz" class="mt-10 flex justify-center">
              <router-link 
                :to="`/quiz-results/${story.id}`" 
                class="px-8 py-4 bg-gradient-to-r from-green-500 to-teal-500 text-white text-lg font-bold rounded-full hover:from-green-600 hover:to-teal-600 transition-all shadow-md hover:shadow-lg transform hover:scale-105 inline-flex items-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                View Quiz Results ✨
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppSidebar from '@/components/AppSidebar.vue';
import { inject, ref } from 'vue';
import api from '@/utils/auth-interceptor';

export default {
  name: "StoryDetailPage",
  components: {
    AppSidebar
  },
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  setup() {
    const isSidebarOpen = inject('sidebarState', ref(true));
    return { isSidebarOpen };
  },
  data() {
    return {
      story: {
        title: '',
        introduction: '',
        complete_story: '',
        user_responses: '',
        difficulty_level: 'Beginner',
        generated_on: '',
        has_quiz: false
      },
      loading: true,
      error: null
    };
  },
  methods: {
    async fetchStoryDetails() {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.get(`http://127.0.0.1:8000/api/v1/storybook/story/${this.id}/detail/`, {
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
          },
        });

        if (response.status === 200) {
          this.story = response.data;
        }
      } catch (error) {
        console.error("Error fetching story details:", error);
        this.error = error.response?.data?.detail || "Failed to load story details. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  },
  mounted() {
    this.fetchStoryDetails();
  }
};
</script>