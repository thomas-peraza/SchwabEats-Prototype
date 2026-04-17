<template>
  <div class="max-w-md mx-auto mt-16 bg-white p-8 rounded-2xl shadow-sm border border-slate-200">
    <h1 class="text-3xl font-bold mb-2">Welcome to SchwabEats</h1>
    <p class="text-slate-500 mb-6">Sign in to continue to the prototype.</p>

    <form class="space-y-4">
      <div>
        <label class="block text-sm font-medium mb-1">Email</label>
        <input
          type="email"
          class="w-full border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="thomas@schwab.com"
        />
      </div>

      <div>
        <label class="block text-sm font-medium mb-1">Password</label>
        <input
          type="password"
          class="w-full border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter password"
        />
      </div>

      <div class="flex gap-3 pt-2">
        <router-link
          to="/employee"
          class="flex-1 text-center bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
        >
          Enter Employee Portal
        </router-link>

        <router-link
          to="/vendor-dashboard"
          class="flex-1 text-center bg-slate-900 text-white py-2 rounded-lg hover:bg-slate-700"
        >
          Enter Vendor Portal
        </router-link>
      </div>
    </form>
  </div>
</template>