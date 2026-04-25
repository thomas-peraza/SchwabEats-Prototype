<template>
  <div class="min-h-screen bg-white text-[#4a4a4a]">
    <div class="border border-[#1FABFF] bg-white">
      <div class="flex items-center justify-between px-4 py-3">
        <div>
          <h1 class="text-[2rem] font-semibold leading-none">Vendor Portal</h1>
        </div>
      </div>
    </div>

    <div class="border-x border-b border-[#1FABFF] bg-white px-4 py-3">
      <div class="flex items-start justify-between">
        <div>
          <h2 class="text-3xl font-medium leading-none">Restaurant Name</h2>
          <p class="text-2xl mt-1">Logged in as: Vendor Manager</p>
        </div>
        <img
          src="https://images.unsplash.com/photo-1551782450-a2132b4ba21d?auto=format&fit=crop&w=300&q=80"
          alt="Restaurant Logo"
          class="w-32 h-20 object-cover border-2 border-black"
        />
      </div>
    </div>

    <div class="px-4 pt-2">
      <h3 class="text-2xl mb-2">Navigation</h3>

      <div class="flex gap-3 flex-wrap mb-4">
        <router-link to="/vendor-dashboard" class="bg-[#1FABFF] text-white px-8 py-3 rounded-md text-xl">Dashboard</router-link>
        <router-link to="/vendor-orders" class="bg-[#1FABFF] text-white px-8 py-3 rounded-md text-xl">Orders</router-link>
        <router-link to="/vendor-menu" class="bg-[#1FABFF] text-white px-8 py-3 rounded-md text-xl">Menu</router-link>
        <router-link to="/vendor-reports" class="bg-[#1FABFF] text-white px-8 py-3 rounded-md text-xl">Reports</router-link>
      </div>
    </div>

    <div class="px-4 pb-8">
      <h3 class="text-3xl mb-1">Active Orders</h3>

      <div class="grid grid-cols-[1fr_3fr_2fr_2fr] border border-gray-400 bg-[#EAF5FB] px-3 py-2 text-2xl">
        <div>Order ID</div>
        <div>Items</div>
        <div>Status</div>
        <div>Action</div>
      </div>

      <div
        v-for="order in vendorOrders"
        :key="order.id"
        class="grid grid-cols-[1fr_3fr_2fr_2fr] border border-gray-400 bg-[#EAF5FB] px-3 py-4 mt-2 min-h-[150px] items-center"
      >
        <div class="text-2xl">{{ order.id }}</div>

        <div class="pr-8 text-lg leading-snug max-w-md">
          <ul class="list-disc pl-5">
            <li v-for="item in order.items" :key="item">{{ item }}</li>
          </ul>
          <p class="mt-3 font-semibold">Total: ${{ order.total.toFixed(2) }}</p>
        </div>

        <div class="flex flex-col items-start gap-3">
          <div class="text-2xl">{{ order.status }}</div>

          <div class="w-44 h-5 border border-gray-600 bg-white overflow-hidden">
            <div
              class="h-full"
              :class="getProgressColor(order.status)"
              :style="{ width: getProgressWidth(order.status) }"
            ></div>
          </div>
        </div>

        <div class="flex flex-col items-start gap-3">
          <select
            class="border border-gray-500 bg-white px-3 py-2 text-xl"
            :value="order.status"
            @change="handleStatusChange(order, $event.target.value)"
          >
            <option>Accepted</option>
            <option>Preparing</option>
            <option>Ready</option>
          </select>
        </div>
      </div>
    </div>

    <div
      v-if="showCompletePopup"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50"
    >
      <div class="bg-white border border-gray-500 rounded-md p-8 w-[400px] text-center shadow-lg">
        <h2 class="text-3xl mb-6">Is this order complete?</h2>

        <div class="flex justify-center gap-4">
          <button
            class="bg-[#1FABFF] text-white px-8 py-3 rounded-md text-xl"
            @click="confirmComplete"
          >
            Yes
          </button>

          <button
            class="bg-gray-200 text-[#4a4a4a] px-8 py-3 rounded-md text-xl"
            @click="cancelComplete"
          >
            No
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const menuPool = [
  { name: 'Beef Taco Plate', price: 12.99 },
  { name: 'Chicken Quesadilla', price: 10.49 },
  { name: 'Chips and Guac', price: 5.99 },
  { name: 'Grilled Chicken Bowl', price: 13.49 },
  { name: 'Veggie Protein Bowl', price: 11.99 },
  { name: 'Fruit Cup', price: 4.99 },
  { name: 'Chicken Alfredo', price: 14.99 },
  { name: 'Spaghetti Marinara', price: 11.49 },
  { name: 'Garlic Bread', price: 4.49 }
]

function randomId() {
  return String(Math.floor(10000000 + Math.random() * 90000000))
}

function randomOrderItems() {
  const shuffled = [...menuPool].sort(() => 0.5 - Math.random())
  const count = Math.floor(Math.random() * 3) + 1
  return shuffled.slice(0, count)
}

function createOrder(status) {
  const selectedItems = randomOrderItems()
  const total = selectedItems.reduce((sum, item) => sum + item.price, 0)

  return {
    id: randomId(),
    items: selectedItems.map((item) => item.name),
    total,
    status
  }
}

const vendorOrders = ref([
  createOrder('Accepted'),
  createOrder('Preparing'),
  createOrder('Ready'),
  createOrder('Preparing'),
  createOrder('Accepted'),
  createOrder('Preparing'),
  createOrder('Ready')
])

const showCompletePopup = ref(false)
const selectedOrder = ref(null)
const previousStatus = ref('')

function getProgressWidth(status) {
  if (status === 'Accepted') return '33%'
  if (status === 'Preparing') return '66%'
  if (status === 'Ready') return '100%'
  return '0%'
}

function getProgressColor(status) {
  if (status === 'Accepted') return 'bg-[#FFBB00]'
  if (status === 'Preparing') return 'bg-[#FFE500]'
  if (status === 'Ready') return 'bg-[#136315]'
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
}

function confirmComplete() {
  if (!selectedOrder.value) return

  const completedOrder = selectedOrder.value

  const currentReports = JSON.parse(localStorage.getItem('vendorReports')) || {
    ordersToday: 24,
    readyForPickup: 8,
    revenue: 312.45
  }

  currentReports.ordersToday += 1
  currentReports.readyForPickup += 1
  currentReports.revenue += completedOrder.total

  localStorage.setItem('vendorReports', JSON.stringify(currentReports))

  vendorOrders.value = vendorOrders.value.filter(
    (order) => order.id !== completedOrder.id
  )

  selectedOrder.value = null
  showCompletePopup.value = false
}

function cancelComplete() {
  if (selectedOrder.value) {
    selectedOrder.value.status = previousStatus.value
  }

  selectedOrder.value = null
  showCompletePopup.value = false
}
</script>