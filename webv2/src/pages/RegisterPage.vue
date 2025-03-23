<template>
  <div class="min-h-screen flex items-center justify-center bg-cover bg-center relative" 
  style="background-image: url('/images/image2.jpg'); background-size: cover; background-position: center;">
    <div class="absolute inset-0 bg-black bg-opacity-60"></div>
    
    <div class="relative z-10 w-full max-w-4xl px-4 py-8">
      <div class="text-center mb-8">
        <h1 class="text-5xl font-bold text-white mb-2">AI Learn Story</h1>
        <p class="text-xl text-gray-300">Begin your AI learning journey</p>
      </div>
      
      <div class="max-w-md mx-auto bg-white bg-opacity-95 rounded-lg shadow-2xl overflow-hidden">
        <div class="bg-green-600 py-4">
          <h2 class="text-lg font-bold text-center text-white">Enter the World of AI Stories</h2>
        </div>
        
        <div class="px-8 py-6">
          <form @submit.prevent="register">
            <div class="mb-6">
              <label for="username" class="block text-lg font-medium text-gray-700 mb-2">Username</label>
              <div class="relative">
                <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                  </svg>
                </span>
                <input
                  type="text"
                  id="username"
                  v-model="username"
                  class="border border-gray-300 rounded-lg pl-10 pr-4 py-3 w-full focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="Choose a username"
                  required
                />
              </div>
            </div>
            
            <div class="mb-6">
              <label for="email" class="block text-lg font-medium text-gray-700 mb-2">Email</label>
              <div class="relative">
                <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                    <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                  </svg>
                </span>
                <input
                  type="email"
                  id="email"
                  v-model="email"
                  class="border border-gray-300 rounded-lg pl-10 pr-4 py-3 w-full focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="Enter your email address"
                  required
                />
              </div>
            </div>
            
            <div class="mb-6">
              <label for="password" class="block text-lg font-medium text-gray-700 mb-2">Password</label>
              <div class="relative">
                <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
                  </svg>
                </span>
                <input
                  type="password"
                  id="password"
                  v-model="password"
                  class="border border-gray-300 rounded-lg pl-10 pr-4 py-3 w-full focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="Create a strong password"
                  required
                />
              </div>
            </div>
            
            <button
              type="submit"
              class="w-full bg-green-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-green-700 transition duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
            >
              Create Account
            </button>
          </form>
          
          <p v-if="errorMessage" class="text-red-500 text-center mt-4 p-2 bg-red-100 rounded">{{ errorMessage }}</p>
          
          <div class="mt-6 text-center">
            <p class="text-gray-600">
              Already have an account? 
              <router-link to="/login" class="text-green-600 font-medium hover:underline">
                Sign in instead
              </router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RegisterPage",
  data() {
    return {
      username: "",
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async register() {
      try {
        await axios.post("http://127.0.0.1:8000/api/v1/accounts/register/", {
          username: this.username,
          email: this.email,
          password: this.password,
        });

        this.$router.push("/login");
      } catch (error) {
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.username
            ? error.response.data.username[0]
            : "An error occurred. Please try again.";
        } else {
          this.errorMessage = "An error occurred. Please try again.";
        }
      }
    },
  },
};
</script>