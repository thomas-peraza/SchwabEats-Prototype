<template>
  <div class="bg-white rounded-2xl shadow-sm overflow-hidden border border-slate-200">
    <img :src="vendor.image" :alt="vendor.name" class="w-full h-48 object-cover" />
    <div class="p-5">
      <h3 class="text-xl font-semibold">{{ vendor.name }}</h3>
      <p class="text-slate-500 mt-1">{{ vendor.cuisine }}</p>
      <div class="flex justify-between text-sm text-slate-600 mt-3">
        <span>⭐ {{ vendor.rating }}</span>
        <span>{{ vendor.deliveryTime }}</span>
      </div>
      <router-link
        :to="`/vendors/${vendor.id}/menu`"
        class="inline-block mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
      >
        View Menu
      </router-link>
    </div>
  </div>
</template>

<script setup>
defineProps({
  vendor: {
    type: Object,
    required: true
  }
})
</script>