<template>
  <div class="min-h-screen flex items-center justify-center bg-cover bg-center relative" 
  style="background-image: url('/images/image3.jpg'); background-size: cover; background-position: center;">
    <div class="absolute inset-0 bg-black bg-opacity-60"></div>
    
    <div class="relative z-10 w-full max-w-4xl px-4 py-8">
      <div class="text-center mb-8">
        <h1 class="text-5xl font-bold text-white mb-2">AI Learn Story</h1>
        <p class="text-xl text-gray-300">Discover the power of AI through stories</p>
      </div>
      
      <div class="max-w-md mx-auto bg-white bg-opacity-95 rounded-lg shadow-2xl overflow-hidden">
        <div class="bg-indigo-500 py-4">
  <h2 class="text-lg font-bold text-center text-white">Step Into AI Storytelling</h2>
</div>
        
        <div class="px-8 py-6">
          <form @submit.prevent="login">
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
                  class="border border-gray-300 rounded-lg pl-10 pr-4 py-3 w-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter your username"
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
                  class="border border-gray-300 rounded-lg pl-10 pr-4 py-3 w-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter your password"
                  required
                />
              </div>
            </div>
            
            <button
              type="submit"
              class="w-full bg-indigo-500 text-white font-bold py-3 px-6 rounded-lg hover:bg-blue-700 transition duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
              :disabled="isLoading"
            >
              <span v-if="isLoading" class="flex items-center justify-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Logging in...
              </span>
              <span v-else>Sign In</span>
            </button>
          </form>
          
          <!-- <p v-if="errorMessage" class="text-red-500 text-center mt-4 p-2 bg-red-100 rounded">{{ errorMessage }}</p> -->
          <!-- <p v-if="debugInfo" class="text-xs text-gray-500 mt-4">{{ debugInfo }}</p> -->
          
          <div class="mt-6 text-center">
            <p class="text-gray-600">
              Don't have an account? 
              <router-link to="/register" class="text-indigo-500 font-medium hover:underline">
                Register now
              </router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
      isLoading: false,
      debugInfo: ""
    };
  },
  methods: {
    async login() {
      this.isLoading = true;
      this.errorMessage = "";
      this.debugInfo = "";
      
      try {
        const loginResponse = await fetch("http://127.0.0.1:8000/login/", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        });
        
        if (loginResponse.ok) {
          this.debugInfo = "Login successful, getting JWT token...";
          
          const tokenResponse = await fetch("http://127.0.0.1:8000/api/token/", {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password
            })
          });
          
          if (tokenResponse.ok) {
            const tokenData = await tokenResponse.json();
            
            localStorage.setItem("access_token", tokenData.access);
            localStorage.setItem("refresh_token", tokenData.refresh);
            localStorage.setItem("username", this.username); 
            
            this.debugInfo = "Token obtained, redirecting...";
            // console.log("Login successful, tokens stored");
            
            this.$router.push("/dashboard");
          } else {
            this.errorMessage = "Failed to obtain authentication token";
            console.error("Token fetch failed:", await tokenResponse.text());
          }
        } else {
          try {
            const errorData = await loginResponse.json();
            this.errorMessage = errorData.error || "Login failed";
          } catch (e) {
            this.errorMessage = `Login failed with status: ${loginResponse.status}`;
          }
        }
      } catch (error) {
        console.error("Login failed:", error);
        this.errorMessage = "An error occurred during login. Please try again.";
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>