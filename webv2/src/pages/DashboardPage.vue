<template>
  <div class="min-h-screen flex"
    style="background-image: url('/images/image4.jpg'); background-size: cover; background-position: center;">

    <AppSidebar />
    <div class="flex-1 transition-all duration-300" :class="[isSidebarOpen ? 'ml-64' : 'ml-20']">
      <!-- Authenticated User View -->
      <div v-if="isAuthenticated" class="p-6 max-w-7xl mx-auto">
        <!-- Header Section with Kid-friendly elements -->
        <div class="mb-8 relative overflow-hidden">
          <div class="absolute -top-16 -right-16 w-32 h-32 bg-yellow-200 rounded-full opacity-50"></div>
          <div class="absolute -bottom-20 -left-20 w-40 h-40 bg-blue-200 rounded-full opacity-50"></div>

          <h1 class="text-3xl font-bold text-indigo relative z-10 flex items-center">
            <span class="mr-3">✨</span> Welcome, {{ user.username }}!
          </h1>
          <p class="text-indigo mt-2 relative z-10">Create magical stories and embark on exciting adventures!</p>
        </div>

        <!-- Stats Overview with playful design -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div
            class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl shadow-md p-6 border-2 border-blue-200 transform hover:scale-105 transition-transform duration-300">
            <div class="flex items-center">
              <div class="p-3 rounded-full bg-blue-200 text-blue-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" viewBox="0 0 20 20" fill="currentColor">
                  <path
                    d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
                </svg>
              </div>
              <div class="ml-4">
                <h2 class="text-lg font-bold text-blue-700">Your Stories</h2>
                <p class="text-3xl font-bold text-blue-900">{{ stories.length }}</p>
              </div>
            </div>
          </div>

          <div
            class="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl shadow-md p-6 border-2 border-green-200 transform hover:scale-105 transition-transform duration-300">
            <div class="flex items-center">
              <div class="p-3 rounded-full bg-green-200 text-green-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-4">
                <h2 class="text-lg font-bold text-green-700">Completed</h2>
                <p class="text-3xl font-bold text-green-900">{{stories.filter(s => s.complete_story).length}}</p>
              </div>
            </div>
          </div>

          <div
            class="bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl shadow-md p-6 border-2 border-purple-200 transform hover:scale-105 transition-transform duration-300">
            <div class="flex items-center">
              <div class="p-3 rounded-full bg-purple-200 text-purple-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z"
                    clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-4">
                <h2 class="text-lg font-bold text-purple-700">Quizzes</h2>
                <p class="text-3xl font-bold text-purple-900">{{stories.filter(s => s.has_quiz).length}}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Generated Stories Section with kid-friendly design -->
        <div class="bg-white rounded-3xl shadow-lg border-2 border-indigo-100 mb-8 overflow-hidden relative">
          <!-- Decorative elements -->
          <div class="absolute -top-6 -left-6 w-12 h-12 bg-yellow-200 rounded-full opacity-60"></div>
          <div class="absolute -bottom-6 -right-6 w-16 h-16 bg-pink-200 rounded-full opacity-70"></div>

          <div class="p-6 border-b-2 border-indigo-100 bg-gradient-to-r from-indigo-50 to-purple-50 relative">
            <div class="flex justify-between items-center">
              <h2 class="text-2xl font-bold text-indigo-800 flex items-center">
                <span class="mr-2">📚</span> Your Stories
              </h2>
              <router-link to="/create"
                class="px-4 py-2 bg-indigo-600 text-white rounded-full hover:bg-indigo-700 transition-colors flex items-center shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-300">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                New Story
              </router-link>
            </div>
          </div>

          <div v-if="loading" class="p-8 text-center">
            <div
              class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-indigo-500 border-t-transparent">
            </div>
            <p class="mt-4 text-lg text-indigo-600 font-medium">Loading your magical stories...</p>
          </div>

          <div v-else-if="stories.length === 0" class="p-12 text-center">
            <div class="max-w-md mx-auto">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 mx-auto text-indigo-300" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              <h3 class="mt-6 text-xl font-bold text-indigo-800">No stories yet</h3>
              <p class="mt-3 text-lg text-indigo-600">Let's create your first magical story to begin your adventure!</p>
            </div>
          </div>

          <div v-else class="overflow-x-auto p-4">
            <table class="min-w-full divide-y divide-indigo-100 rounded-lg overflow-hidden">
              <thead class="bg-indigo-50">
                <tr>
                  <th scope="col"
                    class="px-6 py-4 text-left text-sm font-bold text-indigo-700 uppercase tracking-wider">Story Title
                  </th>
                  <th scope="col"
                    class="px-6 py-4 text-left text-sm font-bold text-indigo-700 uppercase tracking-wider">Created</th>
                  <th scope="col"
                    class="px-6 py-4 text-left text-sm font-bold text-indigo-700 uppercase tracking-wider">Status</th>
                  <th scope="col"
                    class="px-6 py-4 text-left text-sm font-bold text-indigo-700 uppercase tracking-wider">Quiz</th>
                  <th scope="col"
                    class="px-6 py-4 text-right text-sm font-bold text-indigo-700 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-indigo-50">
                <tr v-for="story in stories" :key="story.id" class="hover:bg-indigo-50 transition-colors">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-base font-medium text-indigo-800">{{ story.title }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-indigo-600">{{ formatDate(story.generated_on) }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-3 py-1 inline-flex text-sm leading-5 font-bold rounded-full"
                      :class="story.complete_story ? 'bg-green-100 text-green-800 border border-green-300' : 'bg-yellow-100 text-yellow-800 border border-yellow-300'">
                      {{ story.complete_story ? '✓ Complete' : '⋯ In Progress' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span v-if="story.has_quiz" class="px-3 py-1 inline-flex text-sm leading-5 font-bold rounded-full"
                      :class="story.quiz_complete ? 'bg-green-100 text-green-800 border border-green-300' : 'bg-blue-100 text-blue-800 border border-blue-300'">
                      {{ story.quiz_complete ? '✓ Completed' : '? Available' }}
                    </span>
                    <span v-else class="text-sm text-gray-500">-</span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <router-link :to="story.complete_story ? `/story-detail/${story.id}` : `/story/${story.id}`"
                      class="text-indigo-600 hover:text-indigo-900 mr-4 font-bold">
                      {{ story.complete_story ? '📖 Read' : '✏️ Continue' }}
                    </router-link>
                    <router-link v-if="story.has_quiz"
                      :to="story.quiz_complete ? `/quiz-detail/${story.id}` : `/quiz/${story.id}`"
                      class="text-green-600 hover:text-green-900 mr-4 font-bold">
                      ✏️ Quiz
                    </router-link>
                    <button @click="deleteStory(story.id)" class="text-red-600 hover:text-red-900 font-bold">
                      🗑️ Delete
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div v-else class="p-6 max-w-7xl mx-auto">
        <div class="bg-white rounded-3xl shadow-lg border-2 border-indigo-200 p-8 text-center relative overflow-hidden">
          <div class="absolute top-0 right-0 w-32 h-32 bg-yellow-200 rounded-full opacity-30 -mr-10 -mt-10"></div>
          <div class="absolute bottom-0 left-0 w-40 h-40 bg-blue-200 rounded-full opacity-30 -ml-16 -mb-16"></div>

          <div class="max-w-2xl mx-auto relative z-10">
            <div class="bg-indigo-100 text-indigo-600 p-4 rounded-full inline-flex">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-14 w-14" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <h2 class="mt-6 text-4xl font-bold text-indigo-800">Welcome to AI-Learn a Story! <span
                class="text-4xl">📖✨</span></h2>
            <p class="mt-4 text-xl text-indigo-600">Create magical interactive stories and test your knowledge with fun
              quizzes!</p>

            <div class="mt-10 flex justify-center space-x-6">
              <router-link to="/login"
                class="px-8 py-4 bg-indigo-600 text-white text-lg font-bold rounded-full hover:bg-indigo-700 transition-colors shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-300">
                Login
              </router-link>
              <router-link to="/register"
                class="px-8 py-4 bg-purple-600 text-white text-lg font-bold rounded-full hover:bg-purple-700 transition-colors shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-300">
                Register
              </router-link>
            </div>

            <div class="mt-16 max-w-md mx-auto relative">
              <div class="absolute -top-6 -left-6 w-10 h-10 bg-pink-200 rounded-full animate-pulse"></div>
              <div class="absolute -bottom-6 -right-6 w-12 h-12 bg-green-200 rounded-full animate-pulse"
                style="animation-delay: 1s"></div>

              <h3 class="text-2xl font-bold text-indigo-800 mb-6 flex items-center justify-center">
                <span class="mr-2">✨</span> Try it out as a guest <span class="ml-2">✨</span>
              </h3>
              <form @submit.prevent="startGuestStory"
                class="bg-gradient-to-r from-indigo-50 to-purple-50 p-8 rounded-2xl shadow-md border-2 border-indigo-100">
                <div class="mb-6">
                  <label for="guestTitle" class="block text-base font-bold text-indigo-700 mb-3">Enter a story
                    topic:</label>
                  <input type="text" id="guestTitle" v-model="guestStoryTitle"
                    placeholder="e.g., 'A Dragon's Adventure'..."
                    class="w-full px-4 py-3 border-2 border-indigo-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-indigo-700 placeholder-indigo-300"
                    required />
                </div>
                <button type="submit"
                  class="w-full px-6 py-3 bg-green-600 text-white text-lg font-bold rounded-xl hover:bg-green-700 transition-colors shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-300"
                  :disabled="!isValidGuestTitle || creatingStory"
                  :class="{ 'opacity-50 cursor-not-allowed': !isValidGuestTitle || creatingStory }">
                  Begin Your Adventure!
                </button>
              </form>
              <p class="mt-4 text-sm text-indigo-600">
                Note: To save your stories and track progress, please create an account.
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
import { useRouter } from 'vue-router';

export default {
  name: "DashboardPage",
  components: {
    AppSidebar
  },
  setup() {
    const isSidebarOpen = inject('sidebarState', ref(true));
    const router = useRouter();
    return { isSidebarOpen, router };
  },
  data() {
    return {
      isAuthenticated: false,
      user: { username: "" },
      stories: [],
      loading: true,
      newStoryTitle: "",
      guestStoryTitle: "",
      creatingStory: false,
      storyError: "",
      csrfToken: ""
    };
  },
  computed: {
    isValidTitle() {
      return this.validateText(this.newStoryTitle);
    },
    isValidGuestTitle() {
      return this.validateText(this.guestStoryTitle);
    }
  },
  methods: {
    validateText(text) {
      const words = text.trim().split(/\s+/);
      if (words.length < 3) {
        return false;
      }
      const vowels = /[aeiouAEIOU]/;
      return vowels.test(text);
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },
    async checkAuthentication() {
      const token = localStorage.getItem("access_token");
      if (token) {
        this.user.username = localStorage.getItem("username") || "User";
        this.isAuthenticated = true;
        await this.fetchStories();
      } else {
        this.isAuthenticated = false;
      }
      this.loading = false;
    },
    async fetchStories() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/v1/storybook/api/stories/", {
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
          },
        });

        if (response.status === 200) {
          this.stories = response.data || [];
        } else {
          console.error("Failed to fetch stories:", response.status);
          this.stories = [];
        }
      } catch (error) {
        console.error("Error fetching stories:", error);
        this.stories = [];
      }
    },

    async startStory() {
      if (!this.isValidTitle) {
        this.storyError = "Please enter at least 3 words with vowels.";
        return;
      }

      this.creatingStory = true;
      this.storyError = "";

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/v1/storybook/create/",
          { title: this.newStoryTitle },
          {
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
              "Content-Type": "application/json",
            },
          }
        );

        if (response.status === 200 || response.status === 201) {
          const newStory = response.data;

          this.stories.unshift(newStory);

          this.newStoryTitle = "";

          this.router.push(`/story/${newStory.id}`);
        } else {
          this.storyError = "Failed to create story. Please try again.";
        }
      } catch (error) {
        console.error("Error creating story:", error);
        this.storyError = error.response?.data?.detail || "An error occurred. Please try again.";
      } finally {
        this.creatingStory = false;
      }
    },
    async deleteStory(storyId) {
      if (!confirm("Are you sure you want to delete this story? This action cannot be undone.")) {
        return;
      }

      try {
        const response = await axios.delete(`http://127.0.0.1:8000/api/v1/storybook/story/${storyId}/detail/`, {
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
          },
        });

        if (response.status === 204) {
          this.stories = this.stories.filter(story => story.id !== storyId);
          alert("Story deleted successfully.");
        } else {
          console.error("Failed to delete story:", response.status);
          alert("Failed to delete the story. Please try again.");
        }
      } catch (error) {
        console.error("Error deleting story:", error);
        alert(error.response?.data?.detail || "An error occurred while deleting the story.");
      }
    },
    async startGuestStory() {
      if (!this.isValidGuestTitle) {
        alert("Please enter at least 3 words with vowels.");
        return;
      }

      alert("Please log in or register to create stories.");
      this.$router.push("/login");
    }
  },
  async mounted() {
    await this.checkAuthentication();
  }
};
</script>