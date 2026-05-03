<template>
  <div class="min-h-screen bg-gray-100 text-slate-800 px-4 py-6">
    <div class="max-w-6xl mx-auto">
      <router-link
        to="/employee"
        class="inline-block mb-6 bg-white shadow-md px-5 py-3 rounded-xl hover:shadow-lg active:scale-95 transition-transform duration-150"
      >
        ← Back to Restaurants
      </router-link>

      <header class="bg-white rounded-2xl shadow-lg p-6 mb-8">
        <h1 class="text-4xl font-bold text-sky-700">Past Orders</h1>
        <p class="text-slate-500 mt-1">View orders you have previously placed.</p>
      </header>

      <div v-if="pastOrders.length === 0" class="bg-white rounded-2xl shadow-lg p-10 text-center">
        <p class="text-slate-500 text-lg">No past orders yet.</p>
      </div>

      <div v-else class="space-y-5">
        <div
          v-for="order in pastOrders"
          :key="order.id"
          class="bg-white rounded-2xl shadow-lg p-6"
        >
          <div class="flex flex-wrap justify-between gap-4 mb-4">
            <div>
              <h2 class="text-2xl font-semibold">Order #{{ order.id }}</h2>
              <p class="text-slate-500">Employee: {{ order.employeeName }}</p>
              <p class="text-slate-500">Location: {{ order.location }}</p>
            </div>

            <div class="text-right">
              <p class="text-sm text-slate-500">Status</p>
              <p class="text-lg font-semibold text-sky-700">{{ order.status }}</p>
            </div>
          </div>

          <div class="border-t pt-4">
            <h3 class="font-semibold mb-2">Items</h3>

            <ul class="space-y-1">
              <li v-for="item in order.items" :key="item.name" class="flex justify-between">
                <span>{{ item.quantity }}x {{ item.name }}</span>
                <span>${{ (item.price * item.quantity).toFixed(2) }}</span>
              </li>
            </ul>
          </div>

          <div class="border-t mt-4 pt-4 flex justify-between text-xl font-bold">
            <span>Total</span>
            <span>${{ order.total.toFixed(2) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const pastOrders = ref([])

onMounted(() => {
  pastOrders.value = JSON.parse(localStorage.getItem('employeePastOrders')) || []
})
</script>