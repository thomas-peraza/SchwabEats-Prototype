<template>
  <header class="bg-[#455A64] text-white">
    <div class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
      <router-link to="/employee" class="text-2xl font-bold">
        SchwabEats
      </router-link>

      <nav class="flex items-center gap-5 text-sm font-semibold">
        <router-link to="/employee" class="hover:text-sky-200">Employee</router-link>
        <router-link to="/vendors" class="hover:text-sky-200">Vendors</router-link>
        <router-link to="/vendor-dashboard" class="hover:text-sky-200">Vendor Portal</router-link>
      </nav>
    </div>
  </header>
</template>