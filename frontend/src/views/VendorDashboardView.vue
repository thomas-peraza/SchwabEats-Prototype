<template>
  <div class="min-h-screen bg-white text-[#4a4a4a]">
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
          <h2 class="text-3xl font-medium leading-none">Pasta Corner</h2>
          <p class="text-xl mt-1">Vendor Manager</p>
        </div>

        <img
          :src="pastaLogo"
          alt="Pasta Corner Logo"
          class="w-32 h-20 object-cover border-2 border-black"
        />
      </div>
    </div>

    <div class="px-4 pt-5">
      <h3 class="text-2xl mb-2">Navigation</h3>

      <div class="flex gap-3 flex-wrap mb-4">
        <router-link to="/vendor-dashboard" class="bg-sky-200 text-slate-800 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150">
          Dashboard
        </router-link>

        <router-link to="/vendor-orders" class="bg-sky-200 text-slate-800 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150">
          Orders
        </router-link>

        <router-link to="/vendor-menu" class="bg-sky-200 text-slate-800 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150">
          Menu
        </router-link>

        <router-link to="/vendor-reports" class="bg-sky-200 text-slate-800 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150">
          Reports
        </router-link>
      </div>
    </div>

    <div class="px-4 py-8 grid lg:grid-cols-[2fr_1fr] gap-8">
      <section>
        <h3 class="text-3xl font-semibold mb-5">Dashboard</h3>

        <div class="grid gap-6">
          <router-link to="/vendor-orders" class="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl active:scale-[0.98] transition-transform duration-150">
            <div>
              <h4 class="text-3xl font-semibold text-sky-700">Active Orders</h4>
              <p class="text-slate-500 mt-2">View and manage incoming employee orders.</p>
            </div>

            <p class="text-5xl font-bold mt-6">{{ activeOrders }}</p>
          </router-link>

          <router-link to="/vendor-menu" class="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl active:scale-[0.98] transition-transform duration-150">
            <div>
              <h4 class="text-3xl font-semibold text-sky-700">Menu Items</h4>
              <p class="text-slate-500 mt-2">View the current menu items available to employees.</p>
            </div>

            <p class="text-5xl font-bold mt-6">3</p>
          </router-link>

          <router-link to="/vendor-reports" class="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl active:scale-[0.98] transition-transform duration-150">
            <div>
              <h4 class="text-3xl font-semibold text-sky-700">Daily Summary</h4>
              <p class="text-slate-500 mt-2">Track completed orders, sales, and item performance.</p>
            </div>

            <p class="text-5xl font-bold mt-6">{{ reports.ordersToday }}</p>
          </router-link>
        </div>
      </section>

      <aside class="space-y-6">
        <div class="bg-white rounded-2xl shadow-xl p-6">
          <h3 class="text-2xl font-semibold text-sky-700">Revenue</h3>
          <p class="text-5xl font-bold mt-4">${{ reports.revenue.toFixed(2) }}</p>
          <p class="text-slate-500 mt-2">Revenue from completed orders.</p>
        </div>

        <div class="bg-white rounded-2xl shadow-xl p-6">
          <h3 class="text-2xl font-semibold text-sky-700 mb-4">Revenue Trend</h3>

          <svg viewBox="0 0 400 220" class="w-full h-64 bg-gray-50 rounded-xl p-4">
            <polyline
              v-if="linePoints"
              :points="linePoints"
              fill="none"
              stroke="#1FABFF"
              stroke-width="5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />

            <circle
              v-for="point in graphPoints"
              :key="point.x + '-' + point.y"
              :cx="point.x"
              :cy="point.y"
              r="5"
              fill="#455A64"
            />

            <text
              v-if="graphPoints.length === 0"
              x="200"
              y="110"
              text-anchor="middle"
              fill="#64748b"
              font-size="18"
            >
              No revenue data yet
            </text>
          </svg>

          <p class="text-sm text-slate-500 mt-3">
            Updates when an order is marked complete.
          </p>
        </div>

        <div class="bg-white rounded-2xl shadow-xl p-6">
          <h3 class="text-2xl font-semibold text-sky-700">Completed Orders</h3>
          <p class="text-5xl font-bold mt-4">{{ reports.ordersToday }}</p>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import pastaLogo from '@/assets/pasta-logo.avif'

const reports = ref({
  ordersToday: 0,
  readyForPickup: 0,
  revenue: 0
})

const activeOrders = ref(0)
const revenueHistory = ref([])

onMounted(() => {
  const savedReports = JSON.parse(localStorage.getItem('vendorReports'))
  const savedOrders = JSON.parse(localStorage.getItem('vendorOrders'))
  const savedRevenueHistory = JSON.parse(localStorage.getItem('vendorRevenueHistory'))

  if (savedReports) {
    reports.value = savedReports
  }

  activeOrders.value = savedOrders ? savedOrders.length : 0
  revenueHistory.value = savedRevenueHistory || []
})

const graphPoints = computed(() => {
  if (revenueHistory.value.length === 0) return []

  const maxRevenue = Math.max(...revenueHistory.value, 1)

  return revenueHistory.value.map((value, index) => {
    const x =
      revenueHistory.value.length === 1
        ? 200
        : 30 + (index * 340) / (revenueHistory.value.length - 1)

    const y = 190 - (value / maxRevenue) * 160

    return { x, y }
  })
})

const linePoints = computed(() => {
  return graphPoints.value.map((point) => `${point.x},${point.y}`).join(' ')
})
</script>