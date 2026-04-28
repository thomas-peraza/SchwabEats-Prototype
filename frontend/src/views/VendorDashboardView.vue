<template>
  <div class="min-h-screen bg-white  text-[#4a4a4a]">
    <div class="border border-[#1FABFF] bg-sky-700 rounded-sm">
      <div class="flex items-center justify-between px-4 py-3">
        <div>
          <h1 class="text-[2rem] text-white font-semibold leading-none">Vendor Portal</h1>
        </div>
      </div>
    </div>

    <div class="border-x border-b border-sky-200 bg-white px-4 py-3">
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

      <div class="flex gap-3 flex-wrap mb-6">
        <router-link to="/vendor-dashboard"
          class="bg-sky-200 text-slate-800 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150">
          Dashboard
        </router-link>
        <router-link to="/vendor-orders"
          class="bg-sky-200 text-slate-800 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150">
          Orders
        </router-link>
        <router-link to="/vendor-menu"
          class="bg-sky-200 text-slate-800 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150">
          Menu
        </router-link>
        <router-link to="/vendor-reports"
          class="bg-sky-200 text-slate-800 px-8 py-3 rounded-md text-xl active:scale-95 transition-transform duration-150">
          Reports
        </router-link>
      </div>
    </div>

    <div class="px-4 pb-8">
      <h3 class="text-3xl mb-3">Dashboard</h3>

      <div class="flex flex-col gap-5 max-w-4xl">
        <div
          class="bg-white p-6 rounded-xl shadow-[0_10px_30px_rgba(0,0,0,0.3)] active:scale-[0.99] transition-transform duration-150">
          <h4 class="text-2xl mb-2">Active Orders</h4>
          <p class="text-lg">7 Current Orders</p>
        </div>

        <div
          class="bg-white p-6 rounded-xl shadow-[0_10px_30px_rgba(0,0,0,0.3)] active:scale-[0.99] transition-transform duration-150">
          <h4 class="text-2xl mb-2">Menu Items</h4>
          <p class="text-lg">9 Available Items</p>
        </div>

        <div
          class="bg-white p-6 rounded-xl shadow-[0_10px_30px_rgba(0,0,0,0.3)] active:scale-[0.99] transition-transform duration-150">
          <h4 class="text-2xl mb-2">Daily Summary</h4>
          <p class="text-lg">Prototype Vendor Overview</p>
        </div>
      </div>

      <div class="bg-[#EAF5FB] p-5 mt-5 rounded-lg">
        <h4 class="text-2xl mb-2">Quick Actions</h4>
        <div class="flex gap-3 flex-wrap">
          <router-link to="/vendor-orders"
            class="bg-sky-200 text-slate-800 px-6 py-2 rounded-md text-lg active:scale-95 transition-transform duration-150">
            View Orders
          </router-link>
          <router-link to="/vendor-menu"
            class="bg-sky-200 text-slate-800 px-6 py-2 rounded-md text-lg active:scale-95 transition-transform duration-150">
            View Menu
          </router-link>
          <router-link to="/vendor-reports" class="bg-sky-200 text-slate-800 px-6 py-2 rounded-md text-lg active:scale-95 transition-transform duration-150">
            View Reports
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>