<template>
  <div class="min-h-screen bg-gradient-to-b from-pink-50 to-indigo-50 flex">
    <AppSidebar />
    <div class="flex-1 transition-all duration-300" :class="[isSidebarOpen ? 'ml-64' : 'ml-20']">
      <div class="p-6 max-w-4xl mx-auto">
        <div v-if="loading" class="flex justify-center items-center h-64">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-indigo-500 border-t-transparent">
          </div>
          <p class="ml-2 text-indigo-600">Loading quiz results...</p>
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
                <span class="mr-3">🏆</span> Quiz Results: {{ results.story_title }}
              </h2>
              <div>
                <router-link to="/dashboard"
                  class="px-5 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-full hover:from-indigo-700 hover:to-purple-700 transition-all shadow-md hover:shadow-lg transform hover:scale-105">
                  Back to Dashboard
                </router-link>
              </div>
            </div>
          </div>

          <div class="p-6 bg-gradient-to-r from-indigo-50 to-purple-50 border-b-2 border-indigo-100">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="bg-white rounded-xl shadow-sm p-6 border-2 border-indigo-100 text-center">
                <div class="text-5xl font-bold text-indigo-600 mb-2">{{ results.score }}/{{ results.total_questions }}
                </div>
                <div class="text-lg text-indigo-600">Total Score</div>
              </div>

              <div class="bg-white rounded-xl shadow-sm p-6 border-2 border-indigo-100 text-center">
                <div class="text-5xl font-bold text-indigo-600 mb-2">{{ Math.round((results.score /
                  results.total_questions) * 100) }}%</div>
                <div class="text-lg text-indigo-600">Percentage</div>
              </div>

              <div class="bg-white rounded-xl shadow-sm p-6 border-2 border-indigo-100 text-center">
                <div class="text-5xl font-bold mb-2" :class="getGradeColor(results.grade)">{{ results.grade }}</div>
                <div class="text-lg text-indigo-600">Grade</div>
              </div>
            </div>
          </div>

          <div class="p-8 border-b-2 border-indigo-100 relative z-10">
            <h3 class="text-xl font-bold text-indigo-800 mb-4 flex items-center">
              <span class="mr-3">📊</span> Performance Summary
            </h3>
            <div class="bg-indigo-50 rounded-xl p-6 border-2 border-indigo-100">
              <div class="w-full flex items-center">
                <div class="w-full">
                  <div class="mb-6">
                    <div class="flex justify-between items-center mb-2">
                      <div class="font-medium text-indigo-700">Correct Answers</div>
                      <div class="font-medium text-indigo-700">{{ results.score }}</div>
                    </div>
                    <div class="w-full bg-indigo-200 rounded-full h-6">
                      <div class="bg-green-500 h-6 rounded-full flex items-center justify-end pr-3"
                        :style="`width: ${(results.score / results.total_questions) * 100}%`">
                        <span class="text-xs text-white font-bold"
                          v-if="(results.score / results.total_questions) > 0.1">
                          {{ Math.round((results.score / results.total_questions) * 100) }}%
                        </span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <div class="flex justify-between items-center mb-2">
                      <div class="font-medium text-indigo-700">Incorrect Answers</div>
                      <div class="font-medium text-indigo-700">{{ results.total_questions - results.score }}</div>
                    </div>
                    <div class="w-full bg-indigo-200 rounded-full h-6">
                      <div class="bg-red-500 h-6 rounded-full flex items-center justify-end pr-3"
                        :style="`width: ${((results.total_questions - results.score) / results.total_questions) * 100}%`">
                        <span class="text-xs text-white font-bold"
                          v-if="((results.total_questions - results.score) / results.total_questions) > 0.1">
                          {{ Math.round(((results.total_questions - results.score) / results.total_questions) * 100) }}%
                        </span>
                      </div>
                    </div>
                  </div>

            
                </div>
              </div>
            </div>
          </div>

          <div class="p-8 border-b-2 border-indigo-100 relative z-10">
            <h3 class="text-xl font-bold text-indigo-800 mb-4 flex items-center">
              <span class="mr-3">💬</span> Feedback
            </h3>
            <div class="bg-indigo-50 text-indigo-800 p-6 rounded-xl border-2 border-indigo-100">
              <p class="mb-3 whitespace-pre-line">{{ results.feedback }}</p>

              <h4 class="font-semibold mt-4 mb-2 text-indigo-700">Areas to Review:</h4>
              <ul class="space-y-2 text-indigo-700">
                <li v-for="(area, areaIndex) in results.areas_to_review" :key="areaIndex" class="flex items-start">
                  <span class="mr-2 mt-1">📌</span>
                  <span>{{ area }}</span>
                </li>
              </ul>
            </div>
          </div>

          <div class="p-8 relative z-10">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-xl font-bold text-indigo-800 flex items-center">
                <span class="mr-3">📋</span> Question Review
              </h3>
              <div>
                <!-- <button @click="showAnswers = !showAnswers"
                  class="px-5 py-2 bg-gradient-to-r from-purple-100 to-indigo-100 text-indigo-700 rounded-full hover:from-purple-200 hover:to-indigo-200 transition-all font-bold">
                  {{ showAnswers ? 'Hide Answers' : 'Show Answers' }}
                </button> -->
              </div>
            </div>

            <div class="space-y-6">
              <div v-for="(question, questionIndex) in formattedQuestions" :key="questionIndex"
                class="border-2 rounded-xl p-6" :class="{
                  'border-green-200 bg-green-50': question.is_correct,
                  'border-red-200 bg-red-50': !question.is_correct
                }">
                <div class="flex justify-between items-start mb-2">
                  <h4 class="text-lg font-semibold text-indigo-800">Question {{ questionIndex + 1 }}</h4>
                  <span class="px-3 py-1 rounded-full text-xs font-medium"
                    :class="question.is_correct ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                    {{ question.is_correct ? 'Correct' : 'Incorrect' }}
                  </span>
                </div>
                <p class="text-indigo-700">{{ question.question }}</p>

                <ul class="mt-3 space-y-2">
                  <li v-for="(option, optionIndex) in question.options" :key="optionIndex"
                    class="px-4 py-2 rounded-lg border" :class="{
                      'bg-green-200 border-green-400 text-green-900 font-bold': optionIndex === question.correct_index,
                      'bg-red-200 border-red-400 text-red-900': optionIndex === question.selected_index && optionIndex !== question.correct_index,
                      'bg-white border-indigo-200 text-indigo-700': optionIndex !== question.selected_index
                    }">
                    {{ option }}
                  </li>
                </ul>

                <div v-if="question.explanation && showAnswers" class="mt-3 bg-indigo-100 p-4 rounded-lg">
                  <h5 class="font-semibold text-indigo-800">Explanation:</h5>
                  <p class="text-indigo-700">{{ question.explanation }}</p>
                </div>
              </div>
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
  name: "QuizResultsPage",
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
      results: {
        story_id: null,
        story_title: '',
        score: 0,
        total_questions: 0,
        grade: 'N/A',
        feedback: '',
        areas_to_review: [],
        questions: {}
      },
      formattedQuestions: [],
      showAnswers: false,
      loading: true,
      error: null
    };
  },
  methods: {
    async fetchResults() {
      this.loading = true;
      this.error = null;

      try {
        console.log(`Fetching quiz results for story ID: ${this.id}`);
        const response = await axios.get(`http://127.0.0.1:8000/api/v1/storybook/story/${this.id}/quiz/`, {
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`
          }
        });

        console.log("Quiz results API response:", response.data);

        if (response.status === 200) {
          const { story, quiz } = response.data;

          if (!quiz || quiz.score === undefined) {
            this.error = "Quiz data is incomplete or missing. Please take the quiz first.";
            return;
          }

          console.log("User Answers:", quiz.user_answers || {});
          console.log("Questions:", quiz.questions);

          this.results = {
            story_id: story.id,
            story_title: story.title,
            score: quiz.score,
            total_questions: quiz.total_questions,
            grade: this.calculateGrade(quiz.score, quiz.total_questions),
            feedback: this.generateFeedback(quiz.score, quiz.total_questions),
            areas_to_review: this.calculateAreasToReview(),
            questions: quiz.questions || {},
            user_answers: quiz.user_answers || {} 
          };

          this.formatQuestions();

          console.log("Quiz results loaded:", this.results);
        }
      } catch (error) {
        console.error("Error fetching quiz results:", error);
        this.error = error.response?.data?.detail || "Failed to load quiz results. Please try again.";
      } finally {
        this.loading = false;
      }
    },

    formatQuestions() {
      const questionsData = this.results.questions;
      const userAnswers = this.results.user_answers || {};

      this.formattedQuestions = [];

      Object.keys(questionsData).forEach(key => {
        if (key.startsWith('q')) {
          const questionObj = questionsData[key];

          const userAnswerData = userAnswers[key] || {};
          const userAnswer = userAnswerData.user_answer || null;
          const isCorrect = userAnswerData.correct || false;

          const correctLetter = questionObj.answer;
          const correctIndex = correctLetter.charCodeAt(0) - 65; 

          let userAnswerIndex = null;
          if (userAnswer) {
            userAnswerIndex = userAnswer.charCodeAt(0) - 65;
          }

          this.formattedQuestions.push({
            id: key,
            question: questionObj.question,
            options: questionObj.options,
            correct_index: correctIndex,
            user_answer: userAnswerIndex,
            is_correct: isCorrect,
            correct_option: questionObj.options[correctIndex],
            explanation: questionObj.explanation || null
          });
        }
      });

      this.formattedQuestions.sort((a, b) => parseInt(a.id.substring(1)) - parseInt(b.id.substring(1)));
    },

    formatOptionText(option) {
      if (option && typeof option === 'string' && option.length >= 3 && option[1] === '.') {
        return option.substring(3);
      }
      return option;
    },

    calculateAreasToReview() {
      return ["Reading comprehension", "Story details", "Character understanding"];
    },

    generateFeedback(score, total) {
      const percentage = (score / total) * 100;

      if (percentage >= 90) return "Excellent work! You have a strong understanding of the story.";
      if (percentage >= 80) return "Great job! You understand most of the key details.";
      if (percentage >= 70) return "Good effort! Continue practicing to improve your comprehension.";
      if (percentage >= 60) return "You're making progress. Keep reading and practicing!";
      return "Keep practicing! Try reading the story again to improve your understanding.";
    },

    generateExplanation(question) {
      const correctOptionText = this.formatOptionText(question.options[question.correct_index]);
      return `The correct answer is ${String.fromCharCode(65 + question.correct_index)}: ${correctOptionText}. This information is based on the story's content.`;
    },

    calculateGrade(score, totalQuestions) {
      const percentage = (score / totalQuestions) * 100;

      if (percentage >= 90) return "A";
      if (percentage >= 80) return "B";
      if (percentage >= 70) return "C";
      if (percentage >= 60) return "D";
      return "F";
    },

    getGradeColor(grade) {
      if (!grade || typeof grade !== 'string') {
        return 'text-gray-600'; 
      }

      const gradeMap = {
        'A': 'text-green-600',
        'B': 'text-blue-600',
        'C': 'text-yellow-600',
        'D': 'text-orange-600',
        'F': 'text-red-600'
      };

      const firstChar = grade.charAt(0);

      return gradeMap[firstChar] || 'text-gray-600';
    }
  },
  mounted() {
    console.log("QuizResultsPage mounted with story ID:", this.id);
    this.fetchResults();
  }
};
</script>