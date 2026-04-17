<template>
  <div>
    <h1 class="text-3xl font-bold">Approved Vendors</h1>
    <p class="text-slate-500 mt-2">Select a vendor to view the menu.</p>

    <div class="grid md:grid-cols-2 xl:grid-cols-3 gap-6 mt-8">
      <VendorCard v-for="vendor in vendors" :key="vendor.id" :vendor="vendor" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import VendorCard from '../components/VendorCard.vue'
import { getVendors } from '../services/vendorService'

const vendors = ref([])

onMounted(async () => {
  vendors.value = await getVendors()
})
</script>