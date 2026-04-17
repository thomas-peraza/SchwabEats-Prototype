<template>
  <div>
    <h1 class="text-3xl font-bold">Vendor Dashboard</h1>
    <p class="text-slate-500 mt-2">Manage incoming orders and vendor operations.</p>

    <div class="grid md:grid-cols-3 gap-6 mt-8">
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <h2 class="font-semibold text-lg">Incoming Orders</h2>
        <p class="text-slate-500 mt-2">View and update incoming employee orders.</p>
        <router-link to="/vendor-orders" class="inline-block mt-4 text-blue-700 font-medium">
          View Orders →
        </router-link>
      </div>

      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <h2 class="font-semibold text-lg">Menu Updates</h2>
        <p class="text-slate-500 mt-2">Future area for editing availability and pricing.</p>
      </div>

      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <h2 class="font-semibold text-lg">Vendor Reports</h2>
        <p class="text-slate-500 mt-2">Future area for order volume and revenue metrics.</p>
      </div>
    </div>
  </div>
</template>