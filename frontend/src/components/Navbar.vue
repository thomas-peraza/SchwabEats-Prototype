<template>
  <header class="bg-[#455A64] text-white">
    <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">

      <!-- LOGO -->
      <div
        class="flex items-center text-2xl font-bold cursor-pointer h-full"
        @click="goHome"
      >
        <img :src="logo" alt="Schwab Logo" class="h-16 object-contain" />
        <span>SchwabEats</span>
      </div>

      <!-- NAV -->
      <nav v-if="!isLoginPage" class="flex items-center gap-5 text-sm font-semibold">

        <!-- EMPLOYEE VIEW -->
        <template v-if="isEmployee">
          <!-- No navigation buttons (clean UI) -->
        </template>

        <!-- VENDOR VIEW -->
        <template v-else-if="isVendor">
          <!-- No navigation buttons -->
        </template>

        <!-- DEFAULT (fallback, rarely used) -->
        <template v-else>
          <router-link to="/employee" class="hover:text-sky-200">Employee</router-link>
          <router-link to="/vendors" class="hover:text-sky-200">Vendors</router-link>
          <router-link to="/vendor-dashboard" class="hover:text-sky-200">Vendor Portal</router-link>
        </template>

        <!-- LOGOUT ALWAYS VISIBLE -->
        <button
          class="ml-4 bg-sky-200 text-[#455A64] hover:bg-white px-4 py-2 rounded-lg active:scale-95 transition-transform duration-150"
          @click="logout"
        >
          Log Out
        </button>

      </nav>

    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import logo from '../assets/Charles-Schwab-Logo.png'

const route = useRoute()
const router = useRouter()

const isLoginPage = computed(() => route.path === '/')

const isVendor = computed(() => route.path.includes('vendor'))
const isEmployee = computed(() => route.path.includes('employee'))

function goHome() {
  if (isVendor.value) {
    router.push('/vendor-dashboard')
  } else {
    router.push('/employee')
  }
}

function logout() {
  router.push('/')
}
</script>