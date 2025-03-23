<template>
  <div class="min-h-screen bg-gradient-to-b from-pink-50 to-indigo-50 flex">
    <AppSidebar />
    <div class="flex-1 transition-all duration-300" :class="[isSidebarOpen ? 'ml-64' : 'ml-20']">
      <div class="p-6 max-w-4xl mx-auto">
        <div v-if="loading" class="flex justify-center items-center h-64">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-indigo-500 border-t-transparent"></div>
          <p class="ml-2 text-indigo-600 font-medium">Loading story...</p>
        </div>
        
        <div v-else-if="error" class="bg-red-100 text-red-700 p-4 rounded-xl shadow-md mb-6 border-2 border-red-200">
          {{ error }}
        </div>
        
        <div v-else class="bg-white rounded-3xl shadow-lg border-2 border-indigo-100 overflow-hidden relative">
          <!-- Decorative elements -->
          <div class="absolute -top-10 -right-10 w-24 h-24 bg-yellow-200 rounded-full opacity-30"></div>
          <div class="absolute -bottom-10 -left-10 w-28 h-28 bg-blue-200 rounded-full opacity-30"></div>
          
          <!-- Header -->
          <div class="p-6 border-b-2 border-indigo-100 bg-gradient-to-r from-purple-50 to-indigo-50 relative">
            <div class="flex justify-between items-center">
              <h2 class="text-2xl font-bold text-indigo-800 flex items-center">
                <span class="mr-3">📚</span> {{ story.title }}
              </h2>
              <router-link 
                to="/dashboard" 
                class="px-5 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold rounded-full hover:from-indigo-700 hover:to-purple-700 transition-all shadow-md hover:shadow-lg transform hover:scale-105"
              >
                Back to Dashboard
              </router-link>
            </div>
          </div>
          
          <!-- Progress -->
          <div class="px-6 py-3 bg-indigo-50 border-b-2 border-indigo-100">
            <div v-if="story.complete_story" class="text-green-600 font-semibold flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Story Complete! ✨
            </div>
            <div v-else class="text-indigo-600 font-semibold flex items-center">
              <span class="mr-2">🧙</span> Choices remaining: {{ story.steps_remaining }}
            </div>
          </div>
          
          <!-- Story Content -->
          <div class="p-8 relative z-10">
            <div v-if="story.complete_story" class="bg-indigo-50 p-6 rounded-xl border-2 border-indigo-100 whitespace-pre-line shadow-inner text-indigo-800">
              {{ story.complete_story }}
            </div>
            <div v-else-if="story.current_passage" class="bg-indigo-50 p-6 rounded-xl border-2 border-indigo-100 whitespace-pre-line shadow-inner text-indigo-800">
              {{ story.current_passage }}
            </div>
            <div v-else-if="story.introduction" class="bg-indigo-50 p-6 rounded-xl border-2 border-indigo-100 whitespace-pre-line shadow-inner text-indigo-800">
              {{ story.introduction }}
            </div>
            <div v-else class="bg-indigo-50 p-6 rounded-xl border-2 border-indigo-100 text-indigo-400 italic shadow-inner">
              No story content available.
            </div>
            
            <!-- Continuation Interface -->
            <div v-if="!story.complete_story && story.steps_remaining > 0" class="mt-8">
              <form @submit.prevent="continueStory" class="space-y-6">
                <div>
                  <label for="prompt" class="block text-lg font-bold text-indigo-700 mb-3">What should happen next?</label>
                  <input
                    type="text"
                    id="prompt"
                    v-model="userPrompt"
                    class="w-full px-5 py-4 border-2 border-indigo-300 rounded-xl focus:ring-3 focus:ring-indigo-500 focus:border-indigo-500 text-lg text-indigo-700 placeholder-indigo-300"
                    placeholder="Example: The hero decides to help the old woman"
                    required
                  />
                  <p class="mt-3 text-indigo-600 flex items-center">
                    <span class="mr-2">💡</span>
                    Keep your choice simple and clear!
                  </p>
                </div>
                
                <div v-if="story.steps_remaining === 1" class="p-4 bg-yellow-100 text-yellow-800 rounded-xl border-2 border-yellow-200 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  Next choice will end the story! Choose wisely! ✨
                </div>
                
                <div class="flex justify-center">
                  <button 
                    type="submit" 
                    class="px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-lg font-bold rounded-full hover:from-indigo-700 hover:to-purple-700 transition-all shadow-md hover:shadow-lg transform hover:scale-105 flex items-center"
                    :disabled="!isValidPrompt || submitting"
                    :class="{ 'opacity-50 cursor-not-allowed': !isValidPrompt || submitting }"
                  >
                    <svg v-if="submitting" class="animate-spin -ml-1 mr-3 h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    {{ submitting ? 'Creating Magic...' : `Continue Story (${story.steps_remaining} left)` }}
                  </button>
                </div>
              </form>
            </div>
            
            <!-- Story End -->
            <div v-else-if="story.complete_story" class="mt-8 text-center">
              <h3 class="text-xl font-bold text-indigo-800 mb-4">🎉 Story Complete!</h3>
              <router-link 
                :to="`/quiz/${story.id}`" 
                class="px-8 py-4 bg-gradient-to-r from-green-500 to-teal-500 text-white text-lg font-bold rounded-full hover:from-green-600 hover:to-teal-600 transition-all shadow-md hover:shadow-lg transform hover:scale-105 inline-flex items-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                Start Quiz ({{ story.number_of_questions || 20 }} questions)
              </router-link>
            </div>
            
            <!-- Speech-to-Text Controls -->
            <div class="mt-8 p-6 bg-indigo-50 rounded-xl border-2 border-indigo-100">
              <h4 class="text-lg font-bold text-indigo-700 mb-3">Speech-to-Text Magic 🎤</h4>
              <div class="flex items-center space-x-3 mb-3">
                <button 
                  @click="startRecording" 
                  class="px-5 py-2 bg-gradient-to-r from-blue-500 to-indigo-500 text-white font-bold rounded-full hover:from-blue-600 hover:to-indigo-600 transition-all shadow-md hover:shadow-lg"
                  :disabled="isRecording || story.complete_story || story.steps_remaining === 0"
                  :class="{ 'opacity-50 cursor-not-allowed': isRecording || story.complete_story || story.steps_remaining === 0 }"
                >
                  Start Recording
                </button>
                <button 
                  @click="stopRecording" 
                  class="px-5 py-2 bg-gradient-to-r from-red-500 to-pink-500 text-white font-bold rounded-full hover:from-red-600 hover:to-pink-600 transition-all shadow-md hover:shadow-lg"
                  :disabled="!isRecording"
                  :class="{ 'opacity-50 cursor-not-allowed': !isRecording }"
                >
                  Stop Recording
                </button>
              </div>
              <p class="text-indigo-700 font-medium">
                Recognized text: <span class="font-bold">{{ recognizedText || 'Speak now...' }}</span>
              </p>
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
import axios from 'axios';

export default {
  name: "StoryPage",
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
        id: null,
        title: '',
        current_passage: '',
        introduction: '',
        complete_story: '',
        steps_remaining: 0,
        number_of_questions: 20
      },
      userPrompt: '',
      loading: true,
      error: null,
      submitting: false,
      isRecording: false,
      recognition: null,
      recognizedText: ''
    };
  },
  computed: {
    isValidPrompt() {
      return this.validateText(this.userPrompt);
    }
  },
  methods: {
    async fetchStory() {
  this.loading = true;
  this.error = null;
  
  try {   
    console.log(`Fetching story with ID: ${this.id}`);
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/storybook/story/${this.id}/`, {
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("access_token")}`
      }
    });
    
    console.log("Story API response:", response.data);
    
    if (response.status === 200) {
      this.story = response.data;
      
      if (!this.story.current_passage && this.story.introduction) {
        this.story.current_passage = this.story.introduction;
      }
      
      if (!this.story.current_passage && !this.story.introduction) {
        this.story.current_passage = "Your story is ready to begin. What happens next?";
      }
      
      console.log("Story data loaded:", this.story);
    }
  } catch (error) {
    console.error("Error fetching story:", error);
    this.error = error.response?.data?.detail || "Failed to load story. Please try again.";
  } finally {
    this.loading = false;
  }
},

async continueStory() {
  if (!this.isValidPrompt) {
    alert("Please enter a valid continuation prompt (at least 3 words and must contain at least one vowel).");
    return;
  }
  
  this.submitting = true;
  
  try {
    console.log(`Continuing story ${this.id} with prompt: ${this.userPrompt}`);
    
    const response = await axios.post(`http://127.0.0.1:8000/api/v1/storybook/story/${this.id}/`, {
      prompt: this.userPrompt
    }, {
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
        "Content-Type": "application/json" 
      }
    });
    
    console.log("Story continuation response:", response.data);
    
    if (response.status === 200) {
      if (response.data.status === 'complete' && response.data.redirect_to_quiz) {
        await this.fetchStory();
        this.$router.push(`/quiz/${this.story.id}`);
      } else {
        this.story.current_passage = response.data.current_passage || this.story.current_passage;
        this.story.continuation_count = response.data.continuation_count || 0;
        this.story.steps_remaining = response.data.steps_remaining || 0;
        
        this.userPrompt = '';
        this.recognizedText = '';
      }
    }
  } catch (error) {
    console.error("Error continuing story:", error);
    this.error = error.response?.data?.detail || "Failed to continue story. Please try again.";
  } finally {
    this.submitting = false;
  }
},
    
    validateText(text) {
      if (!text) return false;
      
      const words = text.trim().split(/\s+/);
      if (words.length < 3) {
        return false;
      }
      
      const vowels = /[aeiouAEIOU]/;
      return vowels.test(text);
    },
    
    initSpeechRecognition() {
      if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        console.warn("Speech recognition not supported in this browser");
        return;
      }
      
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      this.recognition = new SpeechRecognition();
      
      this.recognition.lang = 'en-US';
      this.recognition.interimResults = true;
      this.recognition.continuous = false;
      
      this.recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        this.recognizedText = transcript;
        this.userPrompt = transcript;
      };
      
      this.recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        this.isRecording = false;
      };
      
      this.recognition.onend = () => {
        this.isRecording = false;
      };
    },
    
    startRecording() {
      if (!this.recognition) {
        this.initSpeechRecognition();
      }
      
      if (this.recognition) {
        this.recognition.start();
        this.isRecording = true;
      }
    },
    
    stopRecording() {
      if (this.recognition) {
        this.recognition.stop();
        this.isRecording = false;
      }
    }
  },
  mounted() {
    console.log("StoryPage mounted with ID:", this.id);
    this.fetchStory();
    this.initSpeechRecognition();
  },
  beforeUnmount() {
    if (this.recognition) {
      this.recognition.stop();
    }
  }
};
  </script>
  
  