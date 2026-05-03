<template>
  <div class="min-h-screen bg-gray-100 text-slate-800 px-4 py-6">
    <div class="max-w-5xl mx-auto">
      <router-link to="/cart"
        class="inline-block mb-6 bg-white shadow-md px-5 py-3 rounded-xl hover:shadow-lg active:scale-95 transition-transform duration-150">
        ← Back to Cart
      </router-link>
      <h1 class="text-4xl font-bold text-sky-700 mb-2">Checkout</h1>
      <p class="text-slate-500 mb-8">Confirm your delivery information.</p>

      <div class="grid lg:grid-cols-[2fr_1fr] gap-8">
        <form class="bg-white rounded-2xl shadow-xl p-6 space-y-5" @submit.prevent="placeOrder">
          <div>
            <label class="block text-sm font-semibold mb-2">Employee Name</label>
            <input v-model="form.name"
              class="w-full border border-slate-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-sky-400"
              placeholder="Employee name" required />
          </div>

          <div>
            <label class="block text-sm font-semibold mb-2">Delivery Location</label>
            <select v-model="form.location"
              class="w-full border border-slate-300 rounded-xl px-4 py-3 bg-white focus:outline-none focus:ring-2 focus:ring-sky-400"
              required>
              <option disabled value="">Select Schwab location</option>
              <option>Dallas-Park Cities Branch</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-semibold mb-2">Delivery Notes</label>
            <textarea v-model="form.notes"
              class="w-full border border-slate-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-sky-400"
              rows="4" placeholder="Leave at pickup table."></textarea>
          </div>

          <button type="submit"
            class="w-full bg-sky-200 text-slate-900 border border-sky-300 py-3 rounded-xl hover:bg-sky-300 active:scale-95 transition-transform duration-150">
            Place Order
          </button>
        </form>

        <aside class="bg-white rounded-2xl shadow-xl p-6 h-fit">
          <h2 class="text-2xl font-semibold mb-5">Final Summary</h2>

          <div class="space-y-3 text-lg">
            <div class="flex justify-between">
              <span>Subtotal:</span>
              <span>${{ subtotal.toFixed(2) }}</span>
            </div>

            <div class="flex justify-between text-green-700">
              <span>Subsidy (80%):</span>
              <span>- ${{ subsidy.toFixed(2) }}</span>
            </div>

            <div class="flex justify-between">
              <span>Co-Pay:</span>
              <span>${{ copay.toFixed(2) }}</span>
            </div>

            <div class="flex justify-between">
              <span>Taxes:</span>
              <span>${{ taxes.toFixed(2) }}</span>
            </div>

            <div class="border-t pt-4 mt-4 flex justify-between text-2xl font-bold">
              <span>Total:</span>
              <span>${{ total.toFixed(2) }}</span>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useCart } from '../composables/useCart'

const router = useRouter()
const { cartItems, subtotal, clearCart } = useCart()

const form = reactive({
  name: '',
  location: '',
  notes: ''
})

const subsidy = computed(() => subtotal.value * 0.8)
const copay = computed(() => (cartItems.value.length > 0 ? 5 : 0))
const taxableAmount = computed(() => subtotal.value - subsidy.value + copay.value)
const taxes = computed(() => taxableAmount.value * 0.0825)
const total = computed(() => taxableAmount.value + taxes.value)

function placeOrder() {
  const orderNumber = String(Math.floor(10000000 + Math.random() * 90000000))

  const newOrder = {
    id: orderNumber,
    employeeName: form.name,
    location: form.location,
    notes: form.notes,
    items: cartItems.value.map((item) => ({
      name: item.name,
      quantity: item.quantity,
      price: item.price
    })),
    total: total.value,
    status: 'Accepted'
  }

  const existingOrders = JSON.parse(localStorage.getItem('vendorOrders')) || []
  existingOrders.push(newOrder)

  localStorage.setItem('vendorOrders', JSON.stringify(existingOrders))

  const existingPastOrders = JSON.parse(localStorage.getItem('employeePastOrders')) || []
  existingPastOrders.unshift(newOrder)
  localStorage.setItem('employeePastOrders', JSON.stringify(existingPastOrders))

  clearCart()

  router.push({
    path: '/order-confirmation',
    query: {
      orderNumber
    }
  })
}
</script>