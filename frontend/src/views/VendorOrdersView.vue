<template>
  <div>
    <h1 class="text-3xl font-bold">Vendor Orders</h1>
    <p class="text-slate-500 mt-2">Incoming orders for fulfillment.</p>

    <div class="space-y-4 mt-8">
      <div
        v-for="order in vendorOrders"
        :key="order.id"
        class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm"
      >
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h3 class="font-semibold text-lg">Order #{{ order.id }}</h3>
            <p class="text-slate-500">{{ order.employeeName }} • {{ order.vendor }}</p>
            <p class="mt-2 font-medium">${{ order.total.toFixed(2) }}</p>
          </div>

          <div class="flex items-center gap-3">
            <StatusBadge :status="order.status" />
            <select
              class="border rounded-lg px-3 py-2"
              :value="order.status"
              @change="updateStatus(order.id, $event.target.value)"
            >
              <option>Accepted</option>
              <option>Preparing</option>
              <option>Ready</option>
              <option>Completed</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import StatusBadge from '../components/StatusBadge.vue'
import { getOrders } from '../services/orderService'

const vendorOrders = ref([])

function updateStatus(orderId, newStatus) {
  const order = vendorOrders.value.find((item) => item.id === orderId)
  if (order) {
    order.status = newStatus
  }
}

onMounted(async () => {
  vendorOrders.value = await getOrders()
})
</script>