<template>
  <div>
    <h1 class="text-3xl font-bold">Your Cart</h1>
    <p class="text-slate-500 mt-2">Review items before checking out.</p>

    <div class="grid lg:grid-cols-[2fr_1fr] gap-8 mt-8">
      <div class="space-y-4">
        <div
          v-for="item in cartItems"
          :key="item.id"
          class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm"
        >
          <div class="flex items-start justify-between gap-4">
            <div>
              <h3 class="font-semibold text-lg">{{ item.name }}</h3>
              <p class="text-slate-500 mt-1">${{ item.price.toFixed(2) }}</p>
            </div>

            <button class="text-red-600 font-medium" @click="removeFromCart(item.id)">
              Remove
            </button>
          </div>

          <div class="flex items-center gap-3 mt-4">
            <button
              class="w-8 h-8 rounded bg-slate-200"
              @click="updateQuantity(item.id, item.quantity - 1)"
            >
              -
            </button>
            <span class="font-medium">{{ item.quantity }}</span>
            <button
              class="w-8 h-8 rounded bg-slate-200"
              @click="updateQuantity(item.id, item.quantity + 1)"
            >
              +
            </button>
          </div>
        </div>

        <div v-if="cartItems.length === 0" class="bg-white border border-slate-200 rounded-xl p-8 text-center">
          <p class="text-slate-500">Your cart is empty.</p>
          <router-link to="/vendors" class="inline-block mt-4 text-blue-700 font-medium">
            Browse Vendors →
          </router-link>
        </div>
      </div>

      <div class="space-y-4">
        <CartSummary :item-count="itemCount" :subtotal="subtotal" />

        <router-link
          v-if="cartItems.length > 0"
          to="/checkout"
          class="block text-center bg-slate-900 text-white py-3 rounded-xl hover:bg-slate-700"
        >
          Proceed to Checkout
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import CartSummary from '../components/CartSummary.vue'
import { useCart } from '../composables/useCart'

const { cartItems, removeFromCart, updateQuantity, itemCount, subtotal } = useCart()
</script>