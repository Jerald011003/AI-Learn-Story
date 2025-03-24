<template>
    <div class="min-h-screen bg-gradient-to-b from-pink-50 to-indigo-50 flex">
      <AppSidebar />
      <div class="flex-1 transition-all duration-300" :class="[isSidebarOpen ? 'ml-64' : 'ml-20']">
        <div class="p-6 max-w-4xl mx-auto">
          <div class="bg-white rounded-3xl shadow-lg border-2 border-indigo-100 overflow-hidden relative">
            <div class="absolute -top-10 -right-10 w-24 h-24 bg-yellow-200 rounded-full opacity-30"></div>
            <div class="absolute -bottom-10 -left-10 w-28 h-28 bg-blue-200 rounded-full opacity-30"></div>
            
            <div class="p-6 border-b-2 border-indigo-100 bg-gradient-to-r from-purple-50 to-indigo-50 relative">
              <h2 class="text-2xl font-bold text-indigo-800 flex items-center">
                <span class="mr-3">✨</span> Create a Magical Story <span class="ml-3">📚</span>
              </h2>
            </div>
            
            <div class="p-8 relative z-10">
              <div class="mb-8 flex justify-center">
                <div class="w-64 h-64 relative">
                  <div class="absolute top-10 left-10 w-44 h-36 bg-blue-100 rounded-lg"></div>
                  <div class="absolute top-0 left-8 w-16 h-16 bg-blue-200 rounded-tl-lg rounded-tr-lg"></div>
                  <div class="absolute top-0 right-8 w-16 h-16 bg-blue-200 rounded-tl-lg rounded-tr-lg"></div>
                  <div class="absolute top-46 left-20 w-24 h-10 bg-blue-300 rounded-t-lg"></div>
                  <div class="absolute top-46 left-28 w-8 h-12 bg-yellow-100 rounded-t-lg"></div>
                  <div class="absolute bottom-10 left-0 w-16 h-16">
                    <div class="w-10 h-10 bg-green-400 rounded-full mx-auto"></div>
                    <div class="w-2 h-6 bg-brown-500 mx-auto"></div>
                  </div>
                  <div class="absolute bottom-8 right-6 w-16 h-16">
                    <div class="w-12 h-12 bg-green-500 rounded-full mx-auto"></div>
                    <div class="w-2 h-8 bg-yellow-800 mx-auto"></div>
                  </div>
                  <div class="absolute top-2 right-2 w-10 h-10 bg-yellow-300 rounded-full"></div>
                </div>
              </div>
              
              <form @submit.prevent="startStory">
                <div class="mb-6">
                  <label for="title" class="block text-lg font-bold text-indigo-700 mb-3">What's your story about?</label>
                  <input
                    type="text"
                    id="title"
                    v-model="newStoryTitle"
                    placeholder="e.g., 'A Brave Knight and a Dragon Friend'..."
                    class="w-full px-5 py-4 border-2 border-indigo-300 rounded-xl focus:ring-3 focus:ring-indigo-500 focus:border-indigo-500 text-lg text-indigo-700 placeholder-indigo-300"
                    required
                  />
                  <p class="mt-3 text-indigo-600 flex items-center">
                    <span class="mr-2">💡</span>
                    Please enter at least 3 words to help our magic story maker create an amazing tale!
                  </p>
                </div>
                
                <div class="flex justify-center">
                  <button
                    type="submit"
                    class="px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-lg font-bold rounded-full hover:from-indigo-700 hover:to-purple-700 transition-all shadow-md hover:shadow-lg transform hover:scale-105"
                    :disabled="!isValidTitle || creatingStory"
                    :class="{ 'opacity-50 cursor-not-allowed': !isValidTitle || creatingStory }"
                  >
                    <svg
                      v-if="creatingStory"
                      class="animate-spin -ml-1 mr-3 h-6 w-6 text-white inline-block"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        class="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        stroke-width="4"
                      ></circle>
                      <path
                        class="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      ></path>
                    </svg>
                    <span v-if="creatingStory">Creating Magic...</span>
                    <span v-else>Begin Your Adventure!</span>
                  </button>
                </div>
              </form>
              
              <div class="mt-10 pt-6 border-t-2 border-indigo-100">
                <h3 class="text-xl font-bold text-indigo-700 mb-4 flex items-center">
                  <span class="mr-2">⚙️</span> Story Options
                </h3>
                
                <div class="space-y-6">
                  <div>
                    <label class="block text-md font-bold text-indigo-700 mb-3">Difficulty Level</label>
                    <div class="flex space-x-4">
                      <button
                        v-for="level in ['Beginner', 'Intermediate', 'Advanced']" 
                        :key="level"
                        @click="setDifficulty(level)"
                        class="px-4 py-2 rounded-full border-2 transition-all"
                        :class="[
                          selectedDifficulty === level 
                            ? 'bg-indigo-100 border-indigo-400 text-indigo-700 font-bold' 
                            : 'bg-white border-indigo-200 text-indigo-500 hover:bg-indigo-50'
                        ]"
                      >
                        {{ level }}
                      </button>
                    </div>
                  </div>
                  
                  <div>
                    <label class="block text-md font-bold text-indigo-700 mb-3">Story Length</label>
                    <div class="flex space-x-4">
                      <button
                        v-for="length in ['Short', 'Medium', 'Long']" 
                        :key="length"
                        @click="setStoryLength(length)"
                        class="px-4 py-2 rounded-full border-2 transition-all"
                        :class="[
                          selectedLength === length 
                            ? 'bg-indigo-100 border-indigo-400 text-indigo-700 font-bold' 
                            : 'bg-white border-indigo-200 text-indigo-500 hover:bg-indigo-50'
                        ]"
                      >
                        {{ length }}
                      </button>
                    </div>
                  </div>
                  
                  <div>
                    <label for="theme" class="block text-md font-bold text-indigo-700 mb-3">Story Theme (Optional)</label>
                    <select
                      id="theme"
                      v-model="selectedTheme"
                      class="w-full px-4 py-3 border-2 border-indigo-300 rounded-xl focus:ring-3 focus:ring-indigo-500 focus:border-indigo-500 text-indigo-700 bg-white"
                    >
                      <option value="">Choose a theme...</option>
                      <option value="fantasy">Fantasy Adventure</option>
                      <option value="space">Space Exploration</option>
                      <option value="mystery">Mystery</option>
                      <option value="animals">Animal Friends</option>
                      <option value="historical">Historical Journey</option>
                    </select>
                  </div>
                  
                  <div class="bg-indigo-50 p-6 rounded-xl border-2 border-indigo-100">
                    <h4 class="text-md font-bold text-indigo-700 mb-4 flex items-center">
                      <span class="mr-2">🎯</span> Learning Focus
                    </h4>
                    
                    <div class="space-y-3">
                      <div class="flex items-center">
                        <input
                          type="checkbox"
                          id="vocabulary"
                          v-model="learningFocus.vocabulary"
                          class="w-5 h-5 text-indigo-600 border-2 border-indigo-300 rounded focus:ring-indigo-500"
                        />
                        <label for="vocabulary" class="ml-2 text-indigo-700">Enhance Vocabulary</label>
                      </div>
                      <div class="flex items-center">
                        <input
                          type="checkbox"
                          id="grammar"
                          v-model="learningFocus.grammar"
                          class="w-5 h-5 text-indigo-600 border-2 border-indigo-300 rounded focus:ring-indigo-500"
                        />
                        <label for="grammar" class="ml-2 text-indigo-700">Practice Grammar</label>
                      </div>
                      <div class="flex items-center">
                        <input
                          type="checkbox"
                          id="comprehension"
                          v-model="learningFocus.comprehension"
                          class="w-5 h-5 text-indigo-600 border-2 border-indigo-300 rounded focus:ring-indigo-500"
                        />
                        <label for="comprehension" class="ml-2 text-indigo-700">Reading Comprehension</label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="mt-8 bg-yellow-50 p-6 rounded-xl border-2 border-yellow-200">
                <h3 class="text-lg font-bold text-yellow-800 mb-3 flex items-center">
                  <span class="mr-2">✨</span> Story Creation Tips
                </h3>
                <ul class="space-y-2 text-yellow-800">
                  <li class="flex items-start">
                    <span class="mr-2 mt-1">🔍</span>
                    <span>Be specific with your story idea for more personalized results</span>
                  </li>
                  <li class="flex items-start">
                    <span class="mr-2 mt-1">🧩</span>
                    <span>Include characters, settings, or themes you're interested in</span>
                  </li>
                  <li class="flex items-start">
                    <span class="mr-2 mt-1">📝</span>
                    <span>Your story will have interactive choices to guide the adventure</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import AppSidebar from '../components/AppSidebar.vue';
  import { inject, ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'CreateStory',
    components: {
      AppSidebar,
    },
    setup() {
      const isSidebarOpen = inject('sidebarState', ref(true));
      const router = useRouter();
      return { isSidebarOpen, router };
    },
    data() {
        return {
    newStoryTitle: '',
    creatingStory: false,
    storyError: '',
    learningFocus: {
      vocabulary: false,
      grammar: false,
      comprehension: false,
    },
    selectedDifficulty: '',
    selectedLength: '',
    selectedTheme: '',
  };
    },
    computed: {
      isValidTitle() {
        const words = this.newStoryTitle.trim().split(/\s+/);
        const vowels = /[aeiouAEIOU]/;
        return words.length >= 3 && vowels.test(this.newStoryTitle);
      },
    },
    methods: {
  async startStory() {
    if (!this.isValidTitle) {
      this.storyError = 'Please enter at least 3 words with vowels.';
      return;
    }

    this.creatingStory = true;
    this.storyError = '';
// push ko lang
    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/api/v1/storybook/create/',
        {   title: this.newStoryTitle,
            difficulty_level: this.selectedDifficulty || 'beginner',
         },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json',
          },
        }
      );

      if (response.status === 200 || response.status === 201) {
        const newStory = response.data;

        // Navigate to the story page using Vue Router
        this.router.push(`/story/${newStory.id}`);
      } else {
        this.storyError = 'Failed to create story. Please try again.';
      }
    } catch (error) {
      console.error('Error creating story:', error);
      this.storyError = error.response?.data?.detail || 'An error occurred. Please try again.';
    } finally {
      this.creatingStory = false;
    }
  },
  setDifficulty(level) {
    this.selectedDifficulty = level;
  },
  setStoryLength(length) {
    this.selectedLength = length;
  },
},
  };
  </script>
