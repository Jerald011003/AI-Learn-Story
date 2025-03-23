<template>
  <div class="min-h-screen bg-gradient-to-b from-pink-50 to-indigo-50 flex">
    <AppSidebar />
    <div class="flex-1 transition-all duration-300" :class="[isSidebarOpen ? 'ml-64' : 'ml-20']">
      <div class="p-6 max-w-4xl mx-auto">
        <div v-if="loading" class="flex justify-center items-center h-64">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-indigo-500 border-t-transparent">
          </div>
          <p class="ml-2 text-indigo-600">Loading quiz...</p>
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
                <span class="mr-3">📝</span> Quiz: {{ quiz.story_title }}
              </h2>
              <div>
                <router-link to="/dashboard"
                  class="px-5 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-full hover:from-indigo-700 hover:to-purple-700 transition-all shadow-md hover:shadow-lg transform hover:scale-105">
                  Back to Dashboard
                </router-link>
              </div>
            </div>
          </div>

          <div class="px-6 py-3 bg-gradient-to-r from-indigo-50 to-purple-50 border-b-2 border-indigo-100">
            <div class="flex items-center justify-between">
              <div class="text-indigo-700 font-semibold">
                Question {{ currentQuestionIndex + 1 }} of {{ quiz.questions.length }}
              </div>
              <div class="text-indigo-700">
                Score: {{ score }}/{{ currentQuestionIndex }}
              </div>
            </div>
            <div class="w-full bg-indigo-200 rounded-full h-2.5 mt-2">
              <div class="bg-indigo-600 h-2.5 rounded-full"
                :style="{ width: `${(currentQuestionIndex / quiz.questions.length) * 100}%` }"></div>
            </div>
          </div>

          <div v-if="!quizCompleted && currentQuestion" class="p-8 relative z-10">
            <div class="mb-6">
              <h3 class="text-xl font-bold text-indigo-800 mb-4">{{ currentQuestion.question }}</h3>
            </div>

            <div class="space-y-4">
              <div v-for="(option, index) in currentQuestion.options" :key="index"
                class="border-2 border-indigo-100 rounded-xl p-4 hover:bg-indigo-50 cursor-pointer transition-colors" :class="{
                  'border-blue-500 bg-blue-50': selectedOption === index,
                  'opacity-70': answered && selectedOption !== index,
                  'border-green-500 bg-green-50': answered && index === currentQuestion.correct_index,
                  'border-red-500 bg-red-50': answered && selectedOption === index && index !== currentQuestion.correct_index
                }" @click="!answered && selectOption(index)">
                <div class="flex items-center">
                  <div class="mr-3 w-8 h-8 rounded-full flex items-center justify-center" :class="{
                    'bg-blue-100 text-blue-600': selectedOption === index && !answered,
                    'bg-green-100 text-green-600': answered && index === currentQuestion.correct_index,
                    'bg-red-100 text-red-600': answered && selectedOption === index && index !== currentQuestion.correct_index,
                    'bg-indigo-100 text-indigo-600': selectedOption !== index && !answered
                  }">
                    {{ String.fromCharCode(65 + index) }}
                  </div>
                  <div class="text-indigo-700">{{ option }}</div>
                </div>
              </div>
            </div>

            <div class="mt-8 flex justify-between">
              <button v-if="answered" @click="nextQuestion"
                class="px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-lg font-bold rounded-full hover:from-indigo-700 hover:to-purple-700 transition-all shadow-md hover:shadow-lg transform hover:scale-105">
                {{ isLastQuestion ? 'Finish Quiz' : 'Next Question' }}
              </button>
              <button v-else @click="submitAnswer"
                class="px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-lg font-bold rounded-full hover:from-indigo-700 hover:to-purple-700 transition-all shadow-md hover:shadow-lg transform hover:scale-105"
                :disabled="selectedOption === null"
                :class="{ 'opacity-50 cursor-not-allowed': selectedOption === null }">
                Submit Answer
              </button>
            </div>

            <div v-if="answered" class="mt-6 p-6 rounded-xl border-2"
              :class="isCorrect ? 'bg-green-50 text-green-800 border-green-200' : 'bg-red-50 text-red-800 border-red-200'">
              <div class="font-bold mb-2 text-lg flex items-center">
                <span class="mr-2">{{ isCorrect ? '✅' : '❌' }}</span>
                {{ isCorrect ? 'Correct!' : 'Incorrect!' }}
              </div>
              <div>{{ currentQuestion.explanation }}</div>
            </div>
          </div>

          <div v-if="quizCompleted" class="p-8 text-center">
            <div class="mb-6">
              <div class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-indigo-500 border-t-transparent mb-4">
              </div>
            </div>
            <p class="text-indigo-700 text-lg">Quiz completed! Redirecting to results...</p>
            <div class="mt-4">
              <span class="text-indigo-500">✨ Great job completing the quiz! ✨</span>
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
  name: "QuizPage",
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
      quiz: {
        id: null,
        story_title: '',
        questions: []
      },
      currentQuestionIndex: 0,
      selectedOption: null,
      answered: false,
      isCorrect: false,
      score: 0,
      quizCompleted: false,
      loading: true,
      error: null,
      answers: []
    };
  },
  computed: {
    currentQuestion() {
      if (this.quiz.questions && this.quiz.questions.length > this.currentQuestionIndex) {
        return this.quiz.questions[this.currentQuestionIndex];
      }
      return null;
    },
    isLastQuestion() {
      return this.currentQuestionIndex === this.quiz.questions.length - 1;
    }
  },
  methods: {
    async fetchQuiz() {
      this.loading = true;
      this.error = null;

      try {
        // console.log(`Fetching quiz for story ID: ${this.id}`);
        const response = await axios.get(`http://127.0.0.1:8000/api/v1/storybook/quiz/${this.id}/`, {
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`
          }
        });

        // console.log("Quiz API response:", response.data);

        if (response.status === 200) {
          const { story, quiz } = response.data;

          const questionsArray = Object.keys(quiz.questions).map((key) => {
            const question = quiz.questions[key];

            let correctIndex = 0;
            if (question.answer && question.answer.length === 1) {
              correctIndex = question.answer.charCodeAt(0) - 65; 
            }

            return {
              question: question.question,
              options: question.options,
              correct_index: correctIndex,
              explanation: question.explanation || ""
            };
          });

          this.quiz = {
            id: quiz.id,
            story_title: story.title,
            questions: questionsArray
          };

          this.answers = new Array(this.quiz.questions.length).fill(null);
          // console.log("Quiz data loaded:", this.quiz);
        }
      } catch (error) {
        if (error.response?.status === 404) {
          this.error = "No quiz available for this story. Please complete the story first.";
        } else {
          this.error = error.response?.data?.detail || "Failed to load quiz. Please try again.";
        }
      } finally {
        this.loading = false;
      }
    },

    selectOption(index) {
      this.selectedOption = index;
    },

    submitAnswer() {
      if (this.selectedOption === null) return;

      this.isCorrect = this.selectedOption === this.currentQuestion.correct_index;

      if (this.isCorrect) {
        this.score++;
      }

      this.answers[this.currentQuestionIndex] = this.selectedOption;

      this.answered = true;
    },

    nextQuestion() {
      this.selectedOption = null;
      this.answered = false;

      if (this.isLastQuestion) {
        this.finishQuiz();
      } else {
        this.currentQuestionIndex++;
      }
    },

    async finishQuiz() {
      this.quizCompleted = true;

      try {
        // console.log("Submitting answers:", this.answers);

        const response = await axios.post(
          `http://127.0.0.1:8000/api/v1/storybook/quiz/${this.id}/`,
          { answers: this.answers },
          {
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
              "Content-Type": "application/json"
            }
          }
        );

        // console.log("Quiz submission response:", response.data);

        localStorage.setItem(`quiz_${this.id}_score`, response.data.score);
        localStorage.setItem(`quiz_${this.id}_total`, response.data.total_questions);

        this.$router.push(`/quiz-results/${this.id}`);
      } catch (error) {
        console.error("Error submitting quiz:", error);
        this.error = error.response?.data?.detail || "Failed to submit quiz. Please try again.";
        this.quizCompleted = false;
      }
    }

  },
  mounted() {
    // console.log("QuizPage mounted with story ID:", this.id);
    this.fetchQuiz();
  }
};
</script>