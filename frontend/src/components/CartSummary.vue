<template>
  <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
    <h3 class="text-lg font-semibold mb-4">Order Summary</h3>
    <div class="flex justify-between text-sm mb-2">
      <span>Items</span>
      <span>{{ itemCount }}</span>
    </div>
    <div class="flex justify-between text-sm mb-2">
      <span>Subtotal</span>
      <span>${{ subtotal.toFixed(2) }}</span>
    </div>
    <div class="flex justify-between text-sm mb-4">
      <span>Estimated Fees</span>
      <span>$0.00</span>
    </div>
    <div class="border-t pt-4 flex justify-between font-semibold text-lg">
      <span>Total</span>
      <span>${{ subtotal.toFixed(2) }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  itemCount: {
    type: Number,
    required: true
  },
  subtotal: {
    type: Number,
    required: true
  }
})
</script>