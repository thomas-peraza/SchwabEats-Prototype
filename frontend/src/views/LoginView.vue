<template>
  <div class="min-h-screen bg-gray-100 text-slate-800 px-4 py-10">
    <div class="max-w-6xl mx-auto grid lg:grid-cols-2 gap-10 items-center">
      <section class="bg-white rounded-2xl shadow-2xl p-8">
        <h1 class="text-4xl font-bold text-sky-700 mb-2">Log in to SchwabEats</h1>
        <p class="text-slate-500 mb-8">Access the employee or vendor ordering portal.</p>

        <div v-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-xl mb-5">
          {{ errorMessage }}
        </div>

        <form class="space-y-5" @submit.prevent="login">
          <div>
            <label class="block text-lg font-semibold mb-2">Login ID</label>
            <input
              v-model="loginId"
              type="text"
              class="w-full border border-slate-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-sky-400"
              placeholder="Enter login ID"
            />
          </div>

          <div>
            <label class="block text-lg font-semibold mb-2">Password</label>
            <input
              v-model="password"
              type="password"
              class="w-full border border-slate-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-sky-400"
              placeholder="Enter password"
            />
          </div>

          <div>
            <label class="block text-lg font-semibold mb-2">Schwab Location</label>
            <select
              v-model="location"
              class="w-full border border-slate-300 rounded-xl px-4 py-3 bg-white focus:outline-none focus:ring-2 focus:ring-sky-400"
            >
              <option disabled value="">Select Schwab location</option>
              <option>Dallas-Park Cities Branch</option>
            </select>
          </div>

          <button
            type="submit"
            class="w-full bg-sky-200 text-slate-900 border border-sky-300 py-3 rounded-xl hover:bg-sky-300 active:scale-95 transition-transform duration-150 font-semibold"
          >
            Log In
          </button>
        </form>
      </section>

      <section class="hidden lg:block">
        <div class="bg-white rounded-2xl shadow-xl p-10">
          <p class="text-xl font-bold text-slate-900 uppercase">
            SchwabEats Employee Dining
          </p>

          <h2 class="text-5xl font-bold mt-6 leading-tight text-slate-900">
            Office food ordering made simple.
          </h2>

          <p class="text-2xl text-slate-600 mt-6 leading-relaxed">
            Browse approved vendors, select meals, use company subsidy support, and track orders from one place.
          </p>

          <div class="mt-10 bg-sky-100 rounded-2xl p-8 flex items-center justify-center">
            <div class="text-8xl">🍽️</div>
          </div>

          <p class="text-sky-700 text-xl font-semibold mt-8">
            Serving the Dallas-Park Cities Branch
          </p>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const loginId = ref('')
const password = ref('')
const location = ref('')
const errorMessage = ref('')

function login() {
  errorMessage.value = ''

  if (!location.value) {
    errorMessage.value = 'Please select a Schwab location.'
    return
  }

  if (loginId.value === 'john-smith123' && password.value === 'jsmith2026') {
    localStorage.setItem('userRole', 'employee')
    localStorage.setItem('userName', 'John Smith')
    router.push('/employee')
    return
  }

  if (loginId.value === 'pasta_corner_dallas_vendor' && password.value === 'PC2026') {
    localStorage.setItem('userRole', 'vendor')
    localStorage.setItem('userName', 'Pasta Corner Dallas Vendor')
    router.push('/vendor-dashboard')
    return
  }

  errorMessage.value = 'Invalid login ID or password.'
}
</script>