<template>
  <div class="min-h-screen bg-gray-100 text-slate-800 px-4 py-10">
    <div class="max-w-6xl mx-auto grid lg:grid-cols-2 gap-10 items-center">
      <section class="bg-white rounded-2xl shadow-2xl p-8">
        <h1 class="text-4xl font-bold text-sky-700 mb-2">SchwabEats Log In</h1>

        <form class="space-y-4">
          <div>
            <label class="block text-lg font-semibold mb-2">Login ID</label>
            <input
              type="text"
              class="w-full border border-slate-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-sky-400"
              placeholder="Enter login ID"
            />
          </div>

          <div>
            <label class="block text-lg font-semibold mb-2">Password</label>
            <input
              type="password"
              class="w-full border border-slate-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-sky-400"
              placeholder="Enter password"
            />
          </div>

          <div>
            <label class="block text-lg font-semibold mb-2">Schwab Location</label>
            <select
              class="w-full border border-slate-300 rounded-xl px-4 py-3 bg-white focus:outline-none focus:ring-2 focus:ring-sky-400"
            >
              <option>Select your location</option>
              <option>Dallas-Park Cities Branch</option>
            </select>
          </div>

          <div class="flex items-center gap-2">
            <input type="checkbox" class="w-4 h-4" />
            <span class="text-slate-600">Remember Login ID</span>
          </div>

          <div class="grid sm:grid-cols-2 gap-4 pt-4">
            <router-link
              to="/employee"
              class="text-center bg-sky-200 text-slate-900 border border-sky-300 py-3 rounded-xl hover:bg-sky-300 active:scale-95 transition-transform duration-150 font-semibold"
            >
              Employee Login
            </router-link>

            <router-link
              to="/vendor-dashboard"
              class="text-center bg-[#455A64] text-white py-3 rounded-xl hover:bg-[#37474F] active:scale-95 transition-transform duration-150 font-semibold"
            >
              Vendor Login
            </router-link>
          </div>

          <div class="text-center pt-6 text-slate-600">
            Forgot
            <span class="text-sky-700 font-semibold">Login ID</span>
            or
            <span class="text-sky-700 font-semibold">Password?</span>
          </div>
        </form>
      </section>

      <section class="hidden lg:block">
        <div class="bg-white rounded-2xl shadow-xl p-10">
          <p class="text-xl font-bold text-slate-900">
            SchwabEats Employee Dining
          </p>

          <h2 class="text-5xl font-bold mt-6 leading-tight text-slate-900">
            Office food ordering made simple.
          </h2>

          <p class="text-2xl text-slate-600 mt-6 leading-relaxed">
            Browse approved vendors, select meals, use company subsidy support, and track orders from one place.
          </p>

          <div class="mt-10 bg-sky-100 rounded-2xl p-8 flex items-center justify-center">
            <div class="text-8xl">🍽️</div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>