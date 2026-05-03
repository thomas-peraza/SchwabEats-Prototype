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
      <h3 class="text-3xl mb-1">Active Orders</h3>

      <div class="grid grid-cols-[1fr_3fr_2fr_2fr] bg-white px-3 py-2 text-2xl rounded-lg shadow-lg">
        <div>Order ID</div>
        <div>Items</div>
        <div>Status</div>
        <div>Action</div>
      </div>

      <div v-for="order in vendorOrders" :key="order.id"
        class="grid grid-cols-[1fr_3fr_2fr_2fr] bg-white px-3 py-4 mt-3 min-h-[150px] items-center rounded-lg shadow-lg">
        <div class="text-2xl">
          {{ order.id }}
        </div>

        <div class="pr-8 text-lg leading-snug max-w-md">
          <ul class="list-disc pl-5">
            <li v-for="item in order.items" :key="item.name">
              {{ item.quantity }}x {{ item.name }}
            </li>
          </ul>

          <p class="mt-3 font-semibold">Total: ${{ order.total.toFixed(2) }}</p>
          <p class="text-sm text-slate-500 mt-1">Employee: {{ order.employeeName }}</p>
        </div>

        <div class="flex flex-col items-start gap-3">
          <div class="text-2xl">{{ order.status }}</div>

          <div class="w-44 h-5 border border-gray-600 bg-white overflow-hidden rounded">
            <div class="h-full" :class="getProgressColor(order.status)"
              :style="{ width: getProgressWidth(order.status) }"></div>
          </div>
        </div>

        <div class="flex flex-col items-start gap-3">
          <select class="border border-gray-500 bg-white px-3 py-2 text-xl rounded-lg" :value="order.status"
            @change="handleStatusChange(order, $event.target.value)">
            <option>Accepted</option>
            <option>Preparing</option>
            <option>Ready</option>
          </select>
        </div>
      </div>

      <div v-if="vendorOrders.length === 0"
        class="bg-white px-4 py-10 mt-3 text-2xl rounded-lg shadow-lg text-center text-slate-500">
        No active orders yet.
      </div>
    </div>

    <div v-if="showCompletePopup" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-8 w-[400px] text-center shadow-2xl">
        <h2 class="text-3xl mb-6">Is this order complete?</h2>

        <div class="flex justify-center gap-4">
          <button
            class="bg-sky-200 text-slate-900 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150"
            @click="confirmComplete">
            Yes
          </button>

          <button
            class="bg-gray-200 text-[#4a4a4a] px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150"
            @click="cancelComplete">
            No
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const vendorOrders = ref([])
const showCompletePopup = ref(false)
const selectedOrder = ref(null)
const previousStatus = ref('')

function loadOrders() {
  vendorOrders.value = JSON.parse(localStorage.getItem('vendorOrders')) || []
}

function saveOrders() {
  localStorage.setItem('vendorOrders', JSON.stringify(vendorOrders.value))
}

onMounted(() => {
  loadOrders()
})

function getProgressWidth(status) {
  if (status === 'Accepted') return '33%'
  if (status === 'Preparing') return '66%'
  if (status === 'Ready') return '100%'
  return '0%'
}

function getProgressColor(status) {
  if (status === 'Accepted') return 'bg-green-500'
  if (status === 'Preparing') return 'bg-yellow-400'
  if (status === 'Ready') return 'bg-blue-500'
  return 'bg-gray-300'
}

function handleStatusChange(order, newStatus) {
  previousStatus.value = order.status

  if (newStatus === 'Ready') {
    selectedOrder.value = order
    showCompletePopup.value = true
    return
  }

  order.status = newStatus
  saveOrders()
}

function confirmComplete() {
  if (!selectedOrder.value) return

  const completedOrder = selectedOrder.value

  const currentReports = JSON.parse(localStorage.getItem('vendorReports')) || {
    ordersToday: 0,
    readyForPickup: 0,
    revenue: 0
  }

  currentReports.ordersToday += 1
  currentReports.readyForPickup += 1
  currentReports.revenue += completedOrder.total

  localStorage.setItem('vendorReports', JSON.stringify(currentReports))

  const revenueHistory = JSON.parse(localStorage.getItem('vendorRevenueHistory')) || []
  revenueHistory.push(currentReports.revenue)
  localStorage.setItem('vendorRevenueHistory', JSON.stringify(revenueHistory))

  const currentItemSales = JSON.parse(localStorage.getItem('vendorItemSales')) || {}

  completedOrder.items.forEach((item) => {
    currentItemSales[item.name] = (currentItemSales[item.name] || 0) + item.quantity
  })

  localStorage.setItem('vendorItemSales', JSON.stringify(currentItemSales))

  vendorOrders.value = vendorOrders.value.filter((order) => order.id !== completedOrder.id)
  saveOrders()

  selectedOrder.value = null
  showCompletePopup.value = false
}

function cancelComplete() {
  selectedOrder.value = null
  showCompletePopup.value = false
}
</script>
