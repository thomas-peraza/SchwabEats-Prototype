<template>
  <div class="min-h-screen bg-gray-100 text-slate-800 px-4 py-6 relative">
    <div
      v-if="showToast"
      class="fixed top-6 right-6 z-50 bg-green-500 text-white px-6 py-4 rounded-xl shadow-xl font-semibold"
    >
      {{ toastMessage }}
    </div>

    <div class="max-w-6xl mx-auto">
      <button
        class="mb-5 bg-white shadow-md px-5 py-3 rounded-xl hover:shadow-lg active:scale-95 transition-transform duration-150"
        @click="router.push('/employee')"
      >
        ← Back to Restaurants
      </button>

      <section class="bg-white rounded-2xl shadow-xl overflow-hidden mb-8">
        <img :src="vendor.image" :alt="vendor.name" class="w-full h-64 object-cover" />

        <div class="p-6">
          <h1 class="text-4xl font-bold text-sky-700">{{ vendor.name }}</h1>
          <p class="text-slate-500 mt-2">
            {{ vendor.cuisine }} | {{ vendor.deliveryTime }} min delivery
          </p>
          <p class="mt-4 text-slate-700">{{ vendor.description }}</p>
        </div>
      </section>

      <section>
        <h2 class="text-3xl font-semibold mb-5">Menu</h2>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="item in menuItems"
            :key="item.id"
            class="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition"
          >
            <img :src="item.image" :alt="item.name" class="w-full h-40 object-cover" />

            <div class="p-5">
              <h3 class="text-xl font-semibold">{{ item.name }}</h3>
              <p class="text-slate-500 mt-2 text-sm">{{ item.description }}</p>
              <p class="text-sky-700 font-bold text-lg mt-4">
                ${{ item.price.toFixed(2) }}
              </p>

              <button
                class="mt-5 w-full bg-sky-200 text-slate-900 border border-sky-300 py-3 rounded-xl hover:bg-sky-300 active:scale-95 transition-transform duration-150"
                @click="handleAddToCart(item)"
              >
                Add to Cart
              </button>
            </div>
          </div>
        </div>

        <router-link
          to="/cart"
          class="inline-block mt-8 bg-slate-900 text-white px-8 py-3 rounded-xl hover:bg-slate-700 active:scale-95 transition-transform duration-150"
        >
          Go to Cart
        </router-link>
      </section>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCart } from '../composables/useCart'
import { getMenuByVendorId } from '../services/menuService'
import { getVendorById } from '../services/vendorService'

const route = useRoute()
const router = useRouter()
const { addToCart } = useCart()

const showToast = ref(false)
const toastMessage = ref('')
let toastTimer = null

const vendor = ref({
  id: Number(route.params.id),
  name: 'Loading vendor...'
})

const menuItems = ref([])

onMounted(async () => {
  vendor.value = (await getVendorById(route.params.id)) || vendor.value
  menuItems.value = await getMenuByVendorId(route.params.id)
})

function handleAddToCart(item) {
  addToCart({
    ...item,
    vendorId: vendor.value.id,
    vendorName: vendor.value.name
  })

  toastMessage.value = `${item.name} added to cart`
  showToast.value = true

  if (toastTimer) {
    clearTimeout(toastTimer)
  }

  toastTimer = setTimeout(() => {
    showToast.value = false
  }, 4000)
}
</script>