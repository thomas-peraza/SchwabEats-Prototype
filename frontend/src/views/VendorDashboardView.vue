<template>
  <div class="min-h-screen bg-white text-[#4a4a4a]">
    <div class="border border-[#1FABFF] bg-white">
      <div class="flex items-center justify-between px-4 py-3">
        <div>
          <h1 class="text-[2rem] font-semibold leading-none">Vendor Portal</h1>
        </div>
      </div>
    </div>

    <div class="border-x border-b border-[#1FABFF] bg-white px-4 py-3">
      <div class="flex items-start justify-between">
        <div>
          <h2 class="text-3xl font-medium leading-none">Restaurant Name</h2>
          <p class="text-2xl mt-1">Logged in as: Vendor Manager</p>
        </div>

        <img
          src="https://images.unsplash.com/photo-1551782450-a2132b4ba21d?auto=format&fit=crop&w=300&q=80"
          alt="Restaurant Logo"
          class="w-32 h-20 object-cover border-2 border-black"
        />
      </div>
    </div>

    <div class="px-4 pt-2">
      <h3 class="text-2xl mb-2">Navigation</h3>

      <div class="flex gap-3 flex-wrap mb-6">
        <router-link
          to="/vendor-dashboard"
          class="bg-[#1FABFF] text-white px-8 py-3 rounded-md text-xl"
        >
          Dashboard
        </router-link>
        <router-link
          to="/vendor-orders"
          class="bg-[#1FABFF] text-white px-8 py-3 rounded-md text-xl"
        >
          Orders
        </router-link>
        <router-link
          to="/vendor-menu"
          class="bg-[#1FABFF] text-white px-8 py-3 rounded-md text-xl"
        >
          Menu
        </router-link>
        <router-link
          to="/vendor-reports"
          class="bg-[#1FABFF] text-white px-8 py-3 rounded-md text-xl"
        >
          Reports
        </router-link>
      </div>
    </div>

    <div class="px-4 pb-8">
      <h3 class="text-3xl mb-3">Dashboard</h3>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-white p-5 rounded-lg shadow-[0_10px_30px_rgba(0,0,0,0.3)]">
          <h4 class="text-2xl mb-2">Active Orders</h4>
          <p class="text-lg">7 Current Orders</p>
        </div>

        <div class="bg-white p-5 rounded-lg shadow-[0_10px_30px_rgba(0,0,0,0.3)]">
          <h4 class="text-2xl mb-2">Menu Items</h4>
          <p class="text-lg">9 Available Items</p>
        </div>

        <div class="bg-white p-5 rounded-lg shadow-[0_10px_30px_rgba(0,0,0,0.3)]">
          <h4 class="text-2xl mb-2">Daily Summary</h4>
          <p class="text-lg">Prototype Vendor Overview</p>
        </div>
      </div>

      <div class="bg-[#EAF5FB] p-5 mt-5">
        <h4 class="text-2xl mb-2">Quick Actions</h4>
        <div class="flex gap-3 flex-wrap">
          <router-link
            to="/vendor-orders"
            class="bg-[#1FABFF] text-white px-6 py-2 rounded-md text-lg"
          >
            View Orders
          </router-link>
          <router-link
            to="/vendor-menu"
            class="bg-[#1FABFF] text-white px-6 py-2 rounded-md text-lg"
          >
            View Menu
          </router-link>
          <router-link
            to="/vendor-reports"
            class="bg-[#1FABFF] text-white px-6 py-2 rounded-md text-lg"
          >
            View Reports
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>