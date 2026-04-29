<template>
  <div class="min-h-screen bg-gray-100 text-slate-800 px-4 py-6">
    <div class="max-w-6xl mx-auto">
      <router-link to="/employee"
        class="inline-block mb-6 bg-white shadow-md px-5 py-3 rounded-xl hover:shadow-lg active:scale-95 transition-transform duration-150">
        ← Back to Dashboard
      </router-link>
      <h1 class="text-4xl font-bold text-sky-700 mb-2">Your Cart</h1>
      <p class="text-slate-500 mb-8">Review your selected items before checkout.</p>

      <div class="grid lg:grid-cols-[2fr_1fr] gap-8">
        <section class="space-y-4">
          <div v-for="item in cartItems" :key="item.id"
            class="bg-white rounded-2xl shadow-lg p-5 flex justify-between gap-5">
            <div>
              <h3 class="text-xl font-semibold">{{ item.name }}</h3>
              <p class="text-slate-500">{{ item.vendorName }}</p>
              <p class="text-sky-700 font-semibold mt-2">${{ item.price.toFixed(2) }}</p>

              <div class="flex items-center gap-3 mt-4">
                <button
                  class="w-9 h-9 bg-sky-200 rounded-lg hover:bg-sky-300 active:scale-95 transition-transform duration-150"
                  @click="updateQuantity(item.id, item.quantity - 1)">
                  -
                </button>

                <span class="font-semibold">{{ item.quantity }}</span>

                <button
                  class="w-9 h-9 bg-sky-200 rounded-lg hover:bg-sky-300 active:scale-95 transition-transform duration-150"
                  @click="updateQuantity(item.id, item.quantity + 1)">
                  +
                </button>
              </div>
            </div>

            <button class="text-red-600 font-semibold active:scale-95 transition-transform duration-150"
              @click="removeFromCart(item.id)">
              Remove
            </button>
          </div>

          <div v-if="cartItems.length === 0" class="bg-white rounded-2xl shadow-lg p-10 text-center">
            <p class="text-slate-500">Your cart is empty.</p>
            <router-link to="/employee"
              class="inline-block mt-5 bg-sky-200 text-slate-900 px-6 py-3 rounded-xl hover:bg-sky-300 active:scale-95 transition-transform duration-150">
              Browse Restaurants
            </router-link>
          </div>
        </section>

        <aside class="bg-white rounded-2xl shadow-xl p-6 h-fit">
          <h2 class="text-2xl font-semibold mb-5">Order Summary</h2>

          <div class="space-y-3 text-lg">
            <div class="flex justify-between">
              <span>Subtotal:</span>
              <span>${{ subtotal.toFixed(2) }}</span>
            </div>

            <div class="flex justify-between text-green-700">
              <span>Schwab Subsidy (80%):</span>
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

          <router-link v-if="cartItems.length > 0" to="/checkout"
            class="block text-center mt-6 bg-slate-900 text-white py-3 rounded-xl hover:bg-slate-700 active:scale-95 transition-transform duration-150">
            Proceed to Checkout
          </router-link>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCart } from '../composables/useCart'
import { useRouter } from 'vue-router'

const { cartItems, removeFromCart, updateQuantity, subtotal } = useCart()
const router = useRouter()

const subsidy = computed(() => subtotal.value * 0.8)
const copay = computed(() => (cartItems.value.length > 0 ? 5 : 0))
const taxableAmount = computed(() => subtotal.value - subsidy.value + copay.value)
const taxes = computed(() => taxableAmount.value * 0.0825)
const total = computed(() => taxableAmount.value + taxes.value)
</script>