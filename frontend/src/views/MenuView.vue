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
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCart } from '../composables/useCart'

const route = useRoute()
const router = useRouter()
const { addToCart } = useCart()

const showToast = ref(false)
const toastMessage = ref('')
let toastTimer = null

function handleAddToCart(item) {
  addToCart({ ...item, vendorName: vendor.value.name })

  toastMessage.value = `${item.name} added to cart`
  showToast.value = true

  if (toastTimer) {
    clearTimeout(toastTimer)
  }

  toastTimer = setTimeout(() => {
    showToast.value = false
  }, 4000)
}

const vendors = [
  {
    id: 1,
    name: 'Taco House',
    cuisine: 'Mexican',
    deliveryTime: 18,
    image:
      'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=1200&q=80',
    description: 'Fresh tacos, quesadillas, chips, guacamole, and Mexican lunch plates.'
  },
  {
    id: 2,
    name: 'Green Bowl',
    cuisine: 'Healthy',
    deliveryTime: 14,
    image:
      'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1200&q=80',
    description: 'Healthy bowls, fresh fruit, grilled chicken, vegetables, and protein options.'
  },
  {
    id: 3,
    name: 'Pasta Corner',
    cuisine: 'Italian',
    deliveryTime: 26,
    image:
      'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?auto=format&fit=crop&w=1200&q=80',
    description: 'Classic pasta dishes, garlic bread, marinara, alfredo, and Italian comfort food.'
  }
]

const allMenuItems = [
  {
    id: 101,
    vendorId: 1,
    name: 'Beef Taco Plate',
    price: 12.99,
    description: 'Three beef tacos with rice and beans.',
    image:
      'https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?auto=format&fit=crop&w=1200&q=80'
  },
  {
    id: 102,
    vendorId: 1,
    name: 'Chicken Quesadilla',
    price: 10.49,
    description: 'Grilled chicken quesadilla served with salsa.',
    image:
      'https://images.unsplash.com/photo-1618040996337-56904b7850b9?auto=format&fit=crop&w=1200&q=80'
  },
  {
    id: 103,
    vendorId: 1,
    name: 'Chips and Guac',
    price: 5.99,
    description: 'Fresh tortilla chips with guacamole.',
    image:
      'https://images.unsplash.com/photo-1600891964599-f61ba0e24092?auto=format&fit=crop&w=1200&q=80'
  },
  {
    id: 201,
    vendorId: 2,
    name: 'Grilled Chicken Bowl',
    price: 13.49,
    description: 'Rice, greens, avocado, and grilled chicken.',
    image:
      'https://images.unsplash.com/photo-1547496502-affa22d38842?auto=format&fit=crop&w=1200&q=80'
  },
  {
    id: 202,
    vendorId: 2,
    name: 'Veggie Protein Bowl',
    price: 11.99,
    description: 'Quinoa, vegetables, hummus, and greens.',
    image:
      'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1200&q=80'
  },
  {
    id: 203,
    vendorId: 2,
    name: 'Fruit Cup',
    price: 4.99,
    description: 'Seasonal fresh fruit mix.',
    image:
      'https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?auto=format&fit=crop&w=1200&q=80'
  },
  {
    id: 301,
    vendorId: 3,
    name: 'Chicken Alfredo',
    price: 14.99,
    description: 'Creamy alfredo pasta with grilled chicken.',
    image:
      'https://images.unsplash.com/photo-1645112411341-6c4fd023714a?auto=format&fit=crop&w=1200&q=80'
  },
  {
    id: 302,
    vendorId: 3,
    name: 'Spaghetti Marinara',
    price: 11.49,
    description: 'Classic spaghetti with marinara sauce.',
    image:
      'https://images.unsplash.com/photo-1622973536968-3ead9e780960?auto=format&fit=crop&w=1200&q=80'
  },
  {
    id: 303,
    vendorId: 3,
    name: 'Garlic Bread',
    price: 4.49,
    description: 'Toasted garlic bread slices.',
    image:
      'https://images.unsplash.com/photo-1573140247632-f8fd74997d5c?auto=format&fit=crop&w=1200&q=80'
  }
]

const vendor = computed(() => {
  return vendors.find((v) => v.id === Number(route.params.id)) || vendors[0]
})

const menuItems = computed(() => {
  return allMenuItems.filter((item) => item.vendorId === Number(route.params.id))
})
</script>