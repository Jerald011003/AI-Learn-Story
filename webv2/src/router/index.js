import { createRouter, createWebHistory } from "vue-router"
import LoginPage from "../pages/LoginPage.vue"
import DashboardPage from "../pages/DashboardPage.vue"
import RegisterPage from "../pages/RegisterPage.vue"
import StoryPage from "../pages/StoryPage.vue"
import StoryDetailPage from "../pages/StoryDetailPage.vue"
import QuizPage from "../pages/QuizPage.vue"
import QuizResultsPage from "../pages/QuizResultsPage.vue";
import QuizDetailPage from "../pages/QuizDetailPage.vue";
import CreateStory from "../pages/CreateStory.vue"

const routes = [
  {
    path: "/login",
    component: LoginPage,
    name: "login",
    props: (route) => ({ returnTo: route.query.returnTo || null }),
  },
  {
    path: "/register",
    component: RegisterPage,
    name: "register",
  },
  {
    path: "/dashboard",
    component: DashboardPage,
    name: "dashboard",
  },
  {
    path: "/story/:id",
    component: StoryPage,
    name: "story",
    props: (route) => ({ id: route.params.id }),
  },
  {
    path: "/story-detail/:id",
    component: StoryDetailPage,
    name: "story-detail",
    props: (route) => ({ id: route.params.id }),
  },
  {
    path: "/quiz/:id",
    component: QuizPage,
    name: "quiz",
    props: (route) => ({ id: route.params.id }),
  },
  {
    path: "/quiz-detail/:id",
    component: QuizDetailPage,
    name: "quiz-detail",
    props: (route) => ({ id: route.params.id }),
  },
  {
    path: "/quiz-results/:id",
    component: QuizResultsPage,
    name: "quiz-results",
    props: (route) => ({ id: route.params.id }),
  },
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/create",
    component: CreateStory,
    name: "create-story",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const publicPages = ["/login", "/register"]
  const authRequired = !publicPages.includes(to.path)
  const loggedIn = localStorage.getItem("access_token")

  if (authRequired && !loggedIn) {
    return next({
      path: "/login",
      query: { returnTo: to.fullPath },
    })
  }

  next()
})

export default router

