<template>
  <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm flex flex-col justify-between">
    <div>
      <h3 class="text-lg font-semibold">{{ item.name }}</h3>
      <p class="text-slate-500 mt-2">{{ item.description }}</p>
      <p class="text-blue-700 font-semibold mt-3">${{ item.price.toFixed(2) }}</p>
    </div>

    <button
      class="mt-4 bg-slate-900 text-white px-4 py-2 rounded-lg hover:bg-slate-700"
      @click="$emit('add', item)"
    >
      Add to Cart
    </button>
  </div>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    required: true
  }
})

defineEmits(['add'])
</script>