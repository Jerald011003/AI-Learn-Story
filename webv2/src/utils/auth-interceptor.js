// auth-interceptor.js
import axios from "axios"
import router from "../router" // Import your Vue Router instance

// Create an axios instance
const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  withCredentials: true,
})

// Add a request interceptor
api.interceptors.request.use(
  (config) => {
    // Add authorization header with JWT token if available
    const token = localStorage.getItem("access_token")
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Add a response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Handle 401 Unauthorized errors
    if (error.response && error.response.status === 401) {
      // Check if the response contains story_id for redirecting back after login
      const storyId = error.response.data?.story_id

      // Clear any stored tokens
      localStorage.removeItem("access_token")
      localStorage.removeItem("refresh_token")

      // Redirect to login page with return URL if available
      if (storyId) {
        router.push(`/login?returnTo=/story/${storyId}`)
      } else {
        router.push("/login")
      }
    }

    return Promise.reject(error)
  },
)

export default api

