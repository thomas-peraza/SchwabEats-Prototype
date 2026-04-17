<template>
  <div>
    <h1 class="text-3xl font-bold">Checkout</h1>
    <p class="text-slate-500 mt-2">Review your delivery details and place the order.</p>

    <div class="grid lg:grid-cols-[2fr_1fr] gap-8 mt-8">
      <form class="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-4" @submit.prevent="handleSubmit">
        <div>
          <label class="block text-sm font-medium mb-1">Employee Name</label>
          <input v-model="form.name" class="w-full border rounded-lg px-4 py-2" placeholder="Thomas Peraza" />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Office Location</label>
          <input v-model="form.location" class="w-full border rounded-lg px-4 py-2" placeholder="Schwab Campus - Building A" />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Delivery Notes</label>
          <textarea
            v-model="form.notes"
            class="w-full border rounded-lg px-4 py-2"
            rows="4"
            placeholder="Leave order at the front desk."
          />
        </div>

        <button
          type="submit"
          class="bg-blue-600 text-white px-5 py-3 rounded-lg hover:bg-blue-700"
        >
          Place Order
        </button>
      </form>

      <CartSummary :item-count="itemCount" :subtotal="subtotal" />
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import CartSummary from '../components/CartSummary.vue'
import { useCart } from '../composables/useCart'
import { submitOrder } from '../services/orderService'

const router = useRouter()
const { cartItems, itemCount, subtotal, clearCart } = useCart()

const form = reactive({
  name: '',
  location: '',
  notes: ''
})

async function handleSubmit() {
  const result = await submitOrder({
    customer: form,
    items: cartItems.value,
    total: subtotal.value
  })

  clearCart()

  router.push({
    path: '/order-confirmation',
    query: { orderNumber: result.orderNumber }
  })
}
</script>