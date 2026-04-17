<template>
  <header class="bg-white border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
      <router-link to="/employee" class="text-2xl font-bold text-blue-700">
        SchwabEats
      </router-link>

      <nav class="flex items-center gap-4 text-sm font-medium">
        <router-link to="/employee" class="hover:text-blue-700">Employee</router-link>
        <router-link to="/vendors" class="hover:text-blue-700">Vendors</router-link>
        <router-link to="/cart" class="hover:text-blue-700">Cart</router-link>
        <router-link to="/vendor-dashboard" class="hover:text-blue-700">Vendor Portal</router-link>
      </nav>
    </div>
  </header>
</template>