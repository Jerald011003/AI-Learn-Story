<template>
  <aside
    :class="[isSidebarOpen ? 'w-64' : 'w-20', 'fixed left-0 top-0 h-screen bg-slate-800 text-white shadow-lg transition-all duration-300 z-10']"
  >
    <div class="p-4 flex items-center justify-between border-b border-slate-700">
      <div class="flex items-center">
        <div
          v-if="isSidebarOpen"
          class="flex-shrink-0 bg-indigo-500 rounded-lg p-2 flex items-center justify-center"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
            />
          </svg>
        </div>
        <h1
          v-if="isSidebarOpen"
          class="ml-3 text-xl font-bold whitespace-nowrap overflow-hidden transition-opacity duration-300"
        >
          AI-Learn
        </h1>
      </div>
      <button
        @click="toggleSidebar"
        class="text-slate-300 focus:outline-none hover:bg-slate-700 p-2 rounded-md transition-colors"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 6h16M4 12h16m-7 6h7"
          />
        </svg>
      </button>
    </div>

    <nav class="mt-6 flex flex-col justify-between h-[calc(100%-5rem)]">
      <ul class="space-y-2 px-2">
        <li>
          <router-link
            to="/dashboard"
            class="flex items-center p-3 rounded-lg transition-colors"
            :class="[isSidebarOpen ? 'justify-start' : 'justify-center']"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
              />
            </svg>
            <span v-if="isSidebarOpen" class="ml-3">Dashboard</span>
          </router-link>
        </li>

        <li>
          <router-link
            to="/create"
            class="flex items-center p-3 rounded-lg transition-colors"
            :class="[isSidebarOpen ? 'justify-start' : 'justify-center']"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"
              />
            </svg>
            <span v-if="isSidebarOpen" class="ml-3">Create Story</span>
          </router-link>
        </li>
      </ul>

      <div class="px-2 mb-6">
        <button
          @click="logout"
          class="flex w-full items-center p-3 rounded-lg text-slate-300 hover:bg-red-600 hover:text-white transition-colors"
          :class="[isSidebarOpen ? 'justify-start' : 'justify-center']"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
            />
          </svg>
          <span v-if="isSidebarOpen" class="ml-3">Logout</span>
        </button>
      </div>
    </nav>
  </aside>
</template>

<script>
import { ref, provide } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "AppSidebar",
  setup() {
    const isSidebarOpen = ref(true);
    const router = useRouter();

    provide('sidebarState', isSidebarOpen);

    const toggleSidebar = () => {
      isSidebarOpen.value = !isSidebarOpen.value;
    };

    const logout = async () => {
      try {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("username");

        router.push("/login");
      } catch (error) {
        console.error("Logout failed:", error);
      }
    };

    return {
      isSidebarOpen,
      toggleSidebar,
      logout,
    };
  },
};
</script>

