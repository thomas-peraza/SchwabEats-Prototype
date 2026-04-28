<template>
  <div class="min-h-screen bg-gray-100 text-slate-800 px-4 py-6 flex items-center justify-center">
    <div class="max-w-2xl w-full bg-white rounded-2xl shadow-2xl p-10 text-center">
      <div class="text-6xl mb-4">✅</div>

      <h1 class="text-4xl font-bold text-green-700">Order Confirmed</h1>

      <p class="text-slate-500 mt-4">
        Your order has been successfully placed.
      </p>

      <p class="text-2xl font-semibold mt-6">
        Order Number: #{{ orderNumber }}
      </p>

      <div class="flex justify-center gap-4 mt-8">
        <router-link
          to="/employee"
          class="bg-sky-200 text-slate-900 border border-sky-300 px-6 py-3 rounded-xl hover:bg-sky-300 active:scale-95 transition-transform duration-150"
        >
          Order Again
        </router-link>

        <router-link
          to="/cart"
          class="bg-slate-900 text-white px-6 py-3 rounded-xl hover:bg-slate-700 active:scale-95 transition-transform duration-150"
        >
          View Cart
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
const orderNumber = route.query.orderNumber || '00000000'
</script>