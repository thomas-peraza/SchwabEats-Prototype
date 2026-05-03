<template>
  <div class="min-h-screen bg-white  text-[#4a4a4a]">
    <div class="border border-[#1FABFF] bg-sky-700 rounded-sm">
      <div class="flex items-center justify-between px-4 py-3">
        <div>
          <h1 class="text-[2rem] text-white font-semibold leading-none">Vendor Portal</h1>
        </div>
      </div>
    </div>

    <div class="border-x border-b border-sky-200 bg-white px-4 py-3">
      <div class="flex items-start justify-between">
        <div>
          <h2 class="text-3xl font-medium leading-none">Restaurant Name</h2>
          <p class="text-xl mt-1">Vendor Manager</p>
        </div>

        <img src="https://images.unsplash.com/photo-1551782450-a2132b4ba21d?auto=format&fit=crop&w=300&q=80"
          alt="Restaurant Logo" class="w-32 h-20 object-cover border-2 border-black" />
      </div>
    </div>

    <div class="px-4 pt-5">
      <h3 class="text-2xl mb-2">Navigation</h3>

      <div class="flex gap-3 flex-wrap mb-4">
        <router-link to="/vendor-dashboard"
          class="bg-sky-200 text-slate-800 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150">
          Dashboard
        </router-link>
        <router-link to="/vendor-orders"
          class="bg-sky-200 text-slate-800 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150">
          Orders
        </router-link>
        <router-link to="/vendor-menu"
          class="bg-sky-200 text-slate-800 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150">
          Menu
        </router-link>
        <router-link to="/vendor-reports"
          class="bg-sky-200 text-slate-800 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150">
          Reports
        </router-link>
      </div>
    </div>

    <div class="px-4 pb-8">
      <h3 class="text-3xl mb-3">Reports</h3>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-white p-5 rounded-xl shadow-xl">
          <h4 class="text-2xl mb-2">Orders Today</h4>
          <p class="text-3xl">{{ reports.ordersToday }}</p>
        </div>

        <div class="bg-white p-5 rounded-xl shadow-xl">
          <h4 class="text-2xl mb-2">Ready for Delivery</h4>
          <p class="text-3xl">{{ reports.readyForDelivery }}</p>
        </div>

        <div class="bg-white p-5 rounded-xl shadow-xl">
          <h4 class="text-2xl mb-2">Revenue</h4>
          <p class="text-3xl">${{ reports.revenue.toFixed(2) }}</p>
        </div>
      </div>

      <div class="mt-10 w-full max-w-6xl mx-auto bg-white rounded-xl shadow-xl p-8">
        <h3 class="text-3xl mb-4">Item Sales</h3>

        <div class="grid grid-cols-[4fr_1fr] bg-[#1FABFF] text-white text-xl font-semibold px-6 py-3 rounded-t-lg">
          <div>Item</div>
          <div>Total Ordered</div>
        </div>

        <div v-for="(count, item) in itemSales" :key="item"
          class="grid grid-cols-[4fr_1fr] px-6 py-3 border-b border-gray-200 text-lg">
          <div>{{ item }}</div>
          <div>{{ count }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const defaultMenuItems = [
  'Beef Taco Plate',
  'Chicken Quesadilla',
  'Chips and Guac',
  'Grilled Chicken Bowl',
  'Veggie Protein Bowl',
  'Fruit Cup',
  'Chicken Alfredo',
  'Spaghetti Marinara',
  'Garlic Bread'
]

const reports = ref({
  ordersToday: 0,
  readyForDelivery: 0,
  revenue: 0
})

const itemSales = ref({})

onMounted(() => {
  const savedReports = JSON.parse(localStorage.getItem('vendorReports'))
  const savedItemSales = JSON.parse(localStorage.getItem('vendorItemSales'))

  if (savedReports) {
    reports.value = savedReports
  }

  const initializedSales = {}

  defaultMenuItems.forEach((item) => {
    initializedSales[item] = 0
  })

  if (savedItemSales) {
    Object.keys(savedItemSales).forEach((item) => {
      initializedSales[item] = savedItemSales[item]
    })
  }

  itemSales.value = initializedSales
})
</script>
