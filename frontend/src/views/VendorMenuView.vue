<template>
  <div class="min-h-screen bg-white text-[#4a4a4a]">
    <div class="border border-[#1FABFF] bg-sky-700 rounded-sm">
      <div class="flex items-center justify-between px-4 py-3">
        <div>
          <h1 class="text-[2rem] text-white font-semibold leading-none">Vendor Portal</h1>
        </div>
      </div>
    </div>

    <div class="border-x border-b border-[#1FABFF] bg-white px-4 py-3">
      <div class="flex items-start justify-between">
        <div>
          <h2 class="text-3xl font-medium leading-none">Restaurant Name</h2>
          <p class="text-xl mt-1">Vendor Manager</p>
        </div>
        <img src="https://images.unsplash.com/photo-1551782450-a2132b4ba21d?auto=format&fit=crop&w=300&q=80"
          alt="Restaurant Logo" class="w-32 h-20 object-cover border-2 border-black" />
      </div>
    </div>

    <div class="px-4 pt-2">
      <h3 class="text-2xl mb-2">Navigation</h3>
      <div class="flex gap-3 flex-wrap mb-4">
        <router-link to="/vendor-dashboard"
          class="bg-sky-200 text-slate-800 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150">Dashboard</router-link>
        <router-link to="/vendor-orders"
          class="bg-sky-200 text-slate-800 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150">Orders</router-link>
        <router-link to="/vendor-menu"
          class="bg-sky-200 text-slate-800 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150">Menu</router-link>
        <router-link to="/vendor-reports"
          class="bg-sky-200 text-slate-800 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150">Reports</router-link>
      </div>
    </div>

    <div class="px-4 pb-8">
      <h3 class="text-3xl mb-3">Menu</h3>

      <div class="grid gap-3">
        <div v-for="item in menuItems" :key="item" class="bg-[#EAF5FB] px-4 py-4 text-2xl">
          {{ item }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const menuItems = [
  'Beef Taco Plate',
  'Chicken Quesadilla',
  'Chips and Guac',
  'Grilled Chicken Bowl',
  'Veggie Protein Bowl',
  'Fruit Cup',
  'Chicken Alfredo',
  'Spaghetti Marinara',
  'Garlic Bread'
]
</script>