<template>
  <div>
    <h1 class="text-3xl font-bold">Employee Dashboard</h1>
    <p class="text-slate-500 mt-2">Browse approved vendors and place your order.</p>

    <div class="grid md:grid-cols-3 gap-6 mt-8">
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <h2 class="font-semibold text-lg">Explore Vendors</h2>
        <p class="text-slate-500 mt-2">Browse restaurants near your office location.</p>
        <router-link to="/vendors" class="inline-block mt-4 text-blue-700 font-medium">
          Go to Vendors →
        </router-link>
      </div>

      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <h2 class="font-semibold text-lg">Current Cart</h2>
        <p class="text-slate-500 mt-2">Review your selected menu items before checkout.</p>
        <router-link to="/cart" class="inline-block mt-4 text-blue-700 font-medium">
          Go to Cart →
        </router-link>
      </div>

      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <h2 class="font-semibold text-lg">Vendor Portal Demo</h2>
        <p class="text-slate-500 mt-2">Switch to the vendor side of the prototype.</p>
        <router-link to="/vendor-dashboard" class="inline-block mt-4 text-blue-700 font-medium">
          Go to Vendor Portal →
        </router-link>
      </div>
    </div>
  </div>
</template>