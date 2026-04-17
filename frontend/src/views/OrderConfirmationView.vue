<template>
  <div class="max-w-2xl mx-auto bg-white border border-slate-200 rounded-2xl p-8 shadow-sm mt-8 text-center">
    <h1 class="text-3xl font-bold text-green-700">Order Confirmed</h1>
    <p class="text-slate-500 mt-3">
      Your prototype order has been placed successfully.
    </p>
    <p class="mt-4 text-lg font-semibold">
      Order Number: #{{ orderNumber }}
    </p>

    <div class="mt-6 flex justify-center gap-4">
      <router-link to="/vendors" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
        Order Again
      </router-link>
      <router-link to="/vendor-orders" class="bg-slate-900 text-white px-4 py-2 rounded-lg hover:bg-slate-700">
        View Vendor Orders
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
const orderNumber = route.query.orderNumber || '00000'
</script>