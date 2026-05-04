<template>
  <div class="min-h-screen bg-gray-100 text-slate-800 px-4 py-6">
    <div class="max-w-7xl mx-auto">
      <header class="bg-white rounded-2xl shadow-lg p-6 mb-6 flex items-center justify-between">
        <div>
          <h1 class="text-4xl font-bold text-sky-700">SchwabEats</h1>
          <p class="text-slate-500 text-2xl mt-1">Hello John!</p>
        </div>
        <div class="flex items-center gap-4">

          <!-- Past Orders -->
          <router-link to="/past-orders"
            class="bg-sky-200 text-slate-900 border border-sky-300 px-5 py-3 rounded-xl hover:bg-sky-300 active:scale-95 transition-transform duration-150">
            Past Orders
          </router-link>

          <!-- Cart -->
          <router-link to="/cart"
            class="relative text-3xl bg-sky-100 hover:bg-sky-200 rounded-full w-14 h-14 flex items-center justify-center shadow-md active:scale-95 transition-transform duration-150">
            🛒

            <span v-if="itemCount > 0"
              class="absolute -top-1 -right-1 bg-red-600 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center">
              {{ itemCount }}
            </span>
          </router-link>

        </div>

      </header>

      <section class="bg-white rounded-2xl shadow-lg p-5 mb-8">
        <h2 class="text-2xl font-semibold mb-4">Vendors</h2>

        <div class="flex flex-col lg:flex-row gap-3">
          <div class="relative flex-1">
            <input v-model="searchQuery" type="text" placeholder="Search Vendors"
              class="w-full border border-slate-300 rounded-xl px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-sky-400"
              @keyup.enter="runSearch" />

            <button class="absolute right-4 top-3 text-xl active:scale-90 transition-transform duration-150"
              @click="runSearch">
              🔍
            </button>
          </div>

          <select v-model="selectedCuisine"
            class="border border-slate-300 rounded-xl px-4 py-3 bg-white focus:outline-none focus:ring-2 focus:ring-sky-400">
            <option value="">Cuisine Type</option>
            <option>Mexican</option>
            <option>Italian</option>
            <option>Healthy</option>
          </select>

          <select v-model="selectedPrice"
            class="border border-slate-300 rounded-xl px-4 py-3 bg-white focus:outline-none focus:ring-2 focus:ring-sky-400">
            <option value="">Price Range</option>
            <option value="low">$</option>
            <option value="medium">$$</option>
            <option value="high">$$$</option>
          </select>

          <select v-model="selectedDistance"
            class="border border-slate-300 rounded-xl px-4 py-3 bg-white focus:outline-none focus:ring-2 focus:ring-sky-400">
            <option value="">Distance</option>
            <option value="near">Under 15 min</option>
            <option value="mid">15-25 min</option>
            <option value="far">25+ min</option>
          </select>

          <button
            class="bg-sky-200 text-slate-900 border border-sky-300 px-5 py-3 rounded-xl hover:bg-sky-300 active:scale-95 transition-transform duration-150"
            @click="clearFilters">
            Clear
          </button>
        </div>
      </section>

      <section class="mb-10">
        <h2 class="text-2xl font-semibold mb-4">Order Again</h2>

        <div v-if="filteredPastOrders.length > 0" class="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <button v-for="restaurant in filteredPastOrders" :key="'past-' + restaurant.id"
            class="bg-white rounded-2xl shadow-lg overflow-hidden text-left hover:shadow-2xl active:scale-95 transition-transform duration-150"
            @click="openRestaurant(restaurant.id)">
            <img :src="restaurant.image" :alt="restaurant.name" class="w-full h-36 object-cover" />

            <div class="p-4">
              <h3 class="text-lg font-semibold">{{ restaurant.name }}</h3>
              <p class="text-sm text-slate-500 mt-1">
                {{ restaurant.cuisine }} | {{ restaurant.deliveryTime }} min delivery
              </p>
              <p class="text-sm text-slate-600 mt-3 leading-snug">
                {{ restaurant.description }}
              </p>
            </div>
          </button>
        </div>

        <div v-else class="bg-white rounded-2xl shadow-lg p-6 text-slate-500">
          No previous orders match your search.
        </div>
      </section>

      <section v-if="!isFiltering" class="mb-10">
        <h2 class="text-2xl font-semibold mb-4">For You</h2>

        <div class="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <button v-for="restaurant in recommendedRestaurants" :key="'recommended-' + restaurant.id"
            class="bg-white rounded-2xl shadow-lg overflow-hidden text-left hover:shadow-2xl active:scale-95 transition-transform duration-150"
            @click="openRestaurant(restaurant.id)">
            <img :src="restaurant.image" :alt="restaurant.name" class="w-full h-36 object-cover" />

            <div class="p-4">
              <h3 class="text-lg font-semibold">{{ restaurant.name }}</h3>
              <p class="text-sm text-slate-500 mt-1">
                {{ restaurant.cuisine }} | {{ restaurant.deliveryTime }} min delivery
              </p>
              <p class="text-sm text-slate-600 mt-3 leading-snug">
                {{ restaurant.description }}
              </p>
            </div>
          </button>
        </div>
      </section>

      <section class="mb-10">
        <h2 class="text-2xl font-semibold mb-4">
          {{ isFiltering ? 'Search Results' : 'Check out local restaurants!' }}
        </h2>

        <div v-if="filteredRestaurants.length > 0" class="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <button v-for="restaurant in filteredRestaurants" :key="'local-' + restaurant.id"
            class="bg-white rounded-2xl shadow-lg overflow-hidden text-left hover:shadow-2xl active:scale-95 transition-transform duration-150"
            @click="openRestaurant(restaurant.id)">
            <img :src="restaurant.image" :alt="restaurant.name" class="w-full h-36 object-cover" />

            <div class="p-4">
              <h3 class="text-lg font-semibold">{{ restaurant.name }}</h3>
              <p class="text-sm text-slate-500 mt-1">
                {{ restaurant.cuisine }} | {{ restaurant.deliveryTime }} min delivery
              </p>
              <p class="text-sm text-slate-600 mt-3 leading-snug">
                {{ restaurant.description }}
              </p>
            </div>
          </button>
        </div>

        <div v-else class="bg-white rounded-2xl shadow-lg p-6 text-slate-500">
          No restaurants match your search.
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCart } from '../composables/useCart'
import { getRankedVendorCatalog, getRecommendedVendors } from '../services/recommendationService'

const router = useRouter()
const { itemCount } = useCart()

const searchQuery = ref('')
const selectedCuisine = ref('')
const selectedPrice = ref('')
const selectedDistance = ref('')
const submittedSearch = ref('')

const restaurants = [
  {
    id: 1,
    name: 'Taco House',
    cuisine: 'Mexican',
    deliveryTime: 18,
    priceRange: 'medium',
    image:
      'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=1200&q=80',
    description: 'Fresh tacos, quesadillas, chips, guacamole, and Mexican lunch plates.'
  },
  {
    id: 2,
    name: 'Green Bowl',
    cuisine: 'Healthy',
    deliveryTime: 14,
    priceRange: 'medium',
    image:
      'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1200&q=80',
    description: 'Healthy bowls, fresh fruit, grilled chicken, vegetables, and protein options.'
  },
  {
    id: 3,
    name: 'Pasta Corner',
    cuisine: 'Italian',
    deliveryTime: 26,
    priceRange: 'high',
    image:
      'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?auto=format&fit=crop&w=1200&q=80',
    description: 'Classic pasta dishes, garlic bread, marinara, alfredo, and Italian comfort food.'
  }
]

const pastOrders = [restaurants[0], restaurants[2], restaurants[1]]
const recommendedRestaurants = ref([restaurants[1], restaurants[0], restaurants[2]])

const activeSearchText = computed(() => {
  return searchQuery.value.trim().toLowerCase()
})

const isFiltering = computed(() => {
  return (
    activeSearchText.value.length > 0 ||
    selectedCuisine.value !== '' ||
    selectedPrice.value !== '' ||
    selectedDistance.value !== ''
  )
})

const filteredPastOrders = computed(() => {
  return pastOrders.filter((restaurant) => matchesFilters(restaurant))
})

const filteredRestaurants = computed(() => {
  return restaurants.filter((restaurant) => matchesFilters(restaurant))
})

onMounted(async () => {
  try {
    const recommended = await getRecommendedVendors()
    recommendedRestaurants.value = recommended.length > 0 ? recommended : restaurants.slice(0, 3)

    const rankedCatalog = await getRankedVendorCatalog()
    if (!isFiltering.value && rankedCatalog.length > 0) {
      // Keep the recommended rail aligned with the backend-ranked catalog.
      recommendedRestaurants.value = rankedCatalog.slice(0, 3)
    }
  } catch {
    recommendedRestaurants.value = restaurants.slice(0, 3)
  }
})

function matchesFilters(restaurant) {
  const search = activeSearchText.value

  const matchesSearch =
    !search ||
    restaurant.name.toLowerCase().startsWith(search) ||
    restaurant.cuisine.toLowerCase().startsWith(search)

  const matchesCuisine = !selectedCuisine.value || restaurant.cuisine === selectedCuisine.value
  const matchesPrice = !selectedPrice.value || restaurant.priceRange === selectedPrice.value

  const matchesDistance =
    !selectedDistance.value ||
    (selectedDistance.value === 'near' && restaurant.deliveryTime < 15) ||
    (selectedDistance.value === 'mid' &&
      restaurant.deliveryTime >= 15 &&
      restaurant.deliveryTime <= 25) ||
    (selectedDistance.value === 'far' && restaurant.deliveryTime > 25)

  return matchesSearch && matchesCuisine && matchesPrice && matchesDistance
}

function runSearch() {
  submittedSearch.value = searchQuery.value.trim()
}

function clearFilters() {
  searchQuery.value = ''
  submittedSearch.value = ''
  selectedCuisine.value = ''
  selectedPrice.value = ''
  selectedDistance.value = ''
}

function openRestaurant(id) {
  router.push(`/vendors/${id}/menu`)
}
</script>