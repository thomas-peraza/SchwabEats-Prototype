<template>
  <div>
    <div class="flex items-center justify-between flex-wrap gap-4">
      <div>
        <h1 class="text-3xl font-bold">{{ vendor?.name || 'Vendor Menu' }}</h1>
        <p class="text-slate-500 mt-2">{{ vendor?.cuisine }} • {{ vendor?.deliveryTime }}</p>
      </div>

      <router-link to="/cart" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
        View Cart
      </router-link>
    </div>

    <div class="grid md:grid-cols-2 xl:grid-cols-3 gap-6 mt-8">
      <MenuItemCard
        v-for="item in items"
        :key="item.id"
        :item="item"
        @add="handleAddToCart"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import MenuItemCard from '../components/MenuItemCard.vue'
import { getVendorById } from '../services/vendorService'
import { getMenuByVendorId } from '../services/menuService'
import { useCart } from '../composables/useCart'

const route = useRoute()
const vendor = ref(null)
const items = ref([])
const { addToCart } = useCart()

function handleAddToCart(item) {
  addToCart(item)
}

onMounted(async () => {
  vendor.value = await getVendorById(route.params.id)
  items.value = await getMenuByVendorId(route.params.id)
})
</script>