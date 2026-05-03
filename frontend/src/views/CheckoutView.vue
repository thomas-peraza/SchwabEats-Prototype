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
          <div v-if="errorMessage" class="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-red-700">
            {{ errorMessage }}
          </div>

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
            class="w-full bg-sky-200 text-slate-900 border border-sky-300 py-3 rounded-xl hover:bg-sky-300 active:scale-95 transition-transform duration-150 disabled:opacity-60 disabled:cursor-not-allowed"
            :disabled="isSubmitting">
            {{ isSubmitting ? 'Placing Order...' : 'Place Order' }}
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
import { computed, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCart } from '../composables/useCart'
import { currentEmployee } from '../data/currentEmployee'
import { vendors } from '../data/vendors'
import { buildBackendVendor } from '../services/recommendationService'
import { quoteOrder, submitOrder } from '../services/orderService'

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

const isSubmitting = ref(false)
const errorMessage = ref('')

function getCartVendorId() {
  const vendorIds = [...new Set(cartItems.value.map((item) => Number(item.vendorId)).filter(Boolean))]
  return vendorIds.length === 1 ? vendorIds[0] : null
}

function getCheckoutVendor() {
  const vendorId = getCartVendorId()
  if (vendorId) {
    return vendors.find((vendor) => vendor.id === vendorId) || null
  }

  const vendorName = cartItems.value[0]?.vendorName
  return vendors.find((vendor) => vendor.name === vendorName) || null
}

async function placeOrder() {
  errorMessage.value = ''

  if (cartItems.value.length === 0) {
    errorMessage.value = 'Your cart is empty.'
    return
  }

  const vendor = getCheckoutVendor()
  if (!vendor) {
    errorMessage.value = 'Select items from a single vendor before checking out.'
    return
  }

  const selectedItemIds = cartItems.value.map((item) => String(item.id))
  const orderPayload = {
    employee: currentEmployee,
    vendor: buildBackendVendor(vendor.id),
    selected_item_ids: selectedItemIds,
    request_time_local: new Date().toISOString(),
    order_total: subtotal.value,
    employee_name: form.name,
    delivery_location: form.location,
    delivery_notes: form.notes,
    items: cartItems.value
  }

  try {
    isSubmitting.value = true
    await quoteOrder(orderPayload)

    const confirmation = await submitOrder(orderPayload)
    const orderNumber = confirmation.order_id || confirmation.orderNumber || String(Date.now())

    const newOrder = {
      id: orderNumber,
      employeeName: form.name,
      location: form.location,
      notes: form.notes,
      vendorId: vendor.id,
      vendorName: vendor.name,
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
  } catch (error) {
    errorMessage.value = error.details?.reasons?.join(', ') || error.message || 'Order failed.'
  } finally {
    isSubmitting.value = false
  }
}
</script>