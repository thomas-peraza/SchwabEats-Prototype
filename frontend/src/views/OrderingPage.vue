<script setup>
import { ref, computed } from 'vue'

const restaurantName = ref('The Grill House')

const menuItems = ref([
  { id: 1, name: 'Burger', price: 12.00, soldOut: false, img: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=200&h=200&fit=crop' },
  { id: 2, name: 'Pasta', price: 15.00, soldOut: true, img: 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=200&h=200&fit=crop' },
  { id: 3, name: 'Salad', price: 10.00, soldOut: false, img: 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=200&h=200&fit=crop' },
  { id: 4, name: 'Sandwich', price: 9.00, soldOut: false, img: 'https://images.unsplash.com/photo-1553909489-cd47e0907980?w=200&h=200&fit=crop' },
  { id: 5, name: 'Soup', price: 7.00, soldOut: false, img: 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=200&h=200&fit=crop' },
])

const cart = ref([])
const allergies = ref('')
const orderSubmitted = ref(false)

const cartTotal = computed(() =>
  cart.value.reduce((sum, item) => sum + item.price * item.qty, 0)
)

const taxAmount = computed(() => cartTotal.value * 0.0825)
const subsidyAmount = computed(() => cartTotal.value * 0.8)
const employeePay = computed(() => Math.min(cartTotal.value, 5))

function addToCart(item) {
  const existing = cart.value.find(c => c.id === item.id)
  if (existing) {
    existing.qty++
  } else {
    cart.value.push({ ...item, qty: 1 })
  }
}

function removeFromCart(id) {
  const idx = cart.value.findIndex(c => c.id === id)
  if (idx === -1) return
  if (cart.value[idx].qty > 1) {
    cart.value[idx].qty--
  } else {
    cart.value.splice(idx, 1)
  }
}

function submitOrder() {
  if (cart.value.length === 0) return
  orderSubmitted.value = true
}

function resetOrder() {
  cart.value = []
  allergies.value = ''
  orderSubmitted.value = false
}
</script>

<template>
  <div class="ordering-page">
    <header class="page-header">
      <div class="header-inner">
        <span class="brand">SchwabEats</span>
        <span class="restaurant-name">{{ restaurantName }}</span>
      </div>
    </header>

    <div v-if="orderSubmitted" class="success-screen">
      <div class="success-card">
        <div class="success-icon">✓</div>
        <h2>Order Placed!</h2>
        <p>Your order has been submitted to {{ restaurantName }}. Estimated delivery: <strong>30–45 min</strong>.</p>
        <button class="btn-primary" @click="resetOrder">Place Another Order</button>
      </div>
    </div>

    <main v-else class="content">
      <section class="card">
        <h2 class="section-title">Our Offerings</h2>
        <ul class="menu-list">
          <li v-for="item in menuItems" :key="item.id" class="menu-item" :class="{ 'sold-out-row': item.soldOut }">
            <img :src="item.img" :alt="item.name" class="item-img" :class="{ 'img-faded': item.soldOut }" />
            <div class="item-info">
              <span class="item-name" :class="{ 'item-name--faded': item.soldOut }">{{ item.name }}</span>
              <span class="item-price">${{ item.price.toFixed(2) }}</span>
            </div>
            <div class="item-action">
              <span v-if="item.soldOut" class="sold-out-label">SOLD OUT</span>
              <div v-else class="qty-control">
                <button class="qty-btn" :disabled="!cart.find(c => c.id === item.id)" @click="removeFromCart(item.id)">−</button>
                <span class="qty-display">{{ cart.find(c => c.id === item.id)?.qty ?? 0 }}</span>
                <button class="qty-btn" @click="addToCart(item)">+</button>
              </div>
            </div>
          </li>
        </ul>
      </section>

      <section class="card">
        <h2 class="section-title">Allergies / Special Requests</h2>
        <textarea v-model="allergies" class="allergies-input" placeholder="e.g. no nuts, extra sauce, gluten-free..." rows="4"></textarea>
      </section>

      <section class="card">
        <h2 class="section-title">Your Cart</h2>
        <div v-if="cart.length === 0" class="empty-cart">No items added yet.</div>
        <ul v-else class="cart-list">
          <li v-for="item in cart" :key="item.id" class="cart-item">
            <span class="cart-item-name">{{ item.name }}<span class="cart-item-qty" v-if="item.qty > 1"> ×{{ item.qty }}</span></span>
            <span class="cart-item-price">${{ (item.price * item.qty).toFixed(2) }}</span>
          </li>
        </ul>
        <div v-if="cart.length > 0" class="cart-breakdown">
          <div class="breakdown-row"><span>Subtotal</span><span>${{ cartTotal.toFixed(2) }}</span></div>
          <div class="breakdown-row"><span>TX Tax (8.25%)</span><span>${{ taxAmount.toFixed(2) }}</span></div>
          <div class="breakdown-row subsidy-row"><span>Schwab Subsidy (80%)</span><span>−${{ subsidyAmount.toFixed(2) }}</span></div>
          <div class="breakdown-row total-row"><span><strong>Your Co-Pay</strong></span><span><strong>${{ employeePay.toFixed(2) }}</strong></span></div>
        </div>
        <button class="btn-submit" :disabled="cart.length === 0" @click="submitOrder">Submit Order</button>
      </section>
    </main>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@600&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.ordering-page {
  min-height: 100vh;
  background: #f5f4f0;
  font-family: 'DM Sans', sans-serif;
  color: #1a1a1a;
  width: 100%;
  overflow-x: hidden;
}

/* HEADER */
.page-header {
  background: #1a1a2e;
  padding: 1.2rem 1.5rem;
  position: sticky;
  top: 0;
  z-index: 10;
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  width: 100%;
}
.header-inner {
  max-width: 100%;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.brand { font-family: 'Playfair Display', serif; color: #f0c040; font-size: 1.5rem; }
.restaurant-name { color: #ccc; font-size: 0.95rem; }

/* MAIN CONTENT */
.content {
  width: 100%;
  padding: 2rem 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* CARDS */
.card {
  background: #fff;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 1px 4px rgba(0,0,0,0.07);
  width: 100%;
}
.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #eee;
  color: #1a1a2e;
}

/* MENU LIST */
.menu-list { list-style: none; display: flex; flex-direction: column; }
.menu-item {
  display: flex;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid #f0f0f0;
  gap: 1.25rem;
}
.menu-item:last-child { border-bottom: none; }
.sold-out-row { opacity: 0.5; }
.item-img { width: 80px; height: 80px; border-radius: 10px; object-fit: cover; flex-shrink: 0; }
.img-faded { filter: grayscale(100%); }
.item-info { display: flex; flex-direction: column; gap: 4px; flex: 1; min-width: 0; }
.item-name { font-weight: 600; font-size: 1rem; }
.item-name--faded { color: #999; }
.item-price { font-size: 0.9rem; color: #555; }
.item-action { display: flex; align-items: center; flex-shrink: 0; }
.sold-out-label { font-size: 0.8rem; font-weight: 700; color: #c0392b; letter-spacing: 0.5px; text-transform: uppercase; }
.qty-control { display: flex; align-items: center; gap: 0.6rem; }
.qty-btn {
  width: 36px; height: 36px;
  border-radius: 8px;
  border: 1px solid #ddd;
  background: #f8f8f8;
  font-size: 1.1rem;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.15s;
  color: #333;
}
.qty-btn:hover:not(:disabled) { background: #1a1a2e; color: #fff; border-color: #1a1a2e; }
.qty-btn:disabled { opacity: 0.3; cursor: default; }
.qty-display { width: 24px; text-align: center; font-weight: 700; font-size: 1rem; }

/* ALLERGIES */
.allergies-input {
  width: 100%;
  padding: 0.9rem 1.1rem;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
  resize: vertical;
  outline: none;
  transition: border-color 0.2s;
  color: #333;
}
.allergies-input:focus { border-color: #1a1a2e; }

/* CART */
.empty-cart { color: #aaa; font-size: 0.95rem; text-align: center; padding: 1.5rem 0; }
.cart-list { list-style: none; display: flex; flex-direction: column; margin-bottom: 1.25rem; }
.cart-item { display: flex; justify-content: space-between; padding: 0.65rem 0; border-bottom: 1px solid #f5f5f5; font-size: 0.95rem; }
.cart-item:last-child { border-bottom: none; }
.cart-item-name { color: #333; font-weight: 500; }
.cart-item-qty { color: #888; font-size: 0.88rem; }
.cart-item-price { color: #333; font-weight: 600; }
.cart-breakdown { border-top: 1px solid #eee; padding-top: 1rem; display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1.5rem; }
.breakdown-row { display: flex; justify-content: space-between; font-size: 0.95rem; color: #555; }
.subsidy-row { color: #27ae60; }
.total-row { border-top: 1px solid #eee; padding-top: 0.75rem; margin-top: 0.25rem; font-size: 1rem; color: #1a1a1a; }
.btn-submit {
  width: 100%;
  padding: 1rem;
  background: #1a1a2e;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-family: 'DM Sans', sans-serif;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-submit:hover:not(:disabled) { background: #2c2c50; }
.btn-submit:disabled { background: #ccc; cursor: default; }

/* SUCCESS */
.success-screen { display: flex; align-items: center; justify-content: center; min-height: calc(100vh - 60px); padding: 2rem 1.5rem; }
.success-card { background: #fff; border-radius: 16px; padding: 3rem 2rem; text-align: center; max-width: 480px; width: 100%; box-shadow: 0 4px 24px rgba(0,0,0,0.08); }
.success-icon { width: 72px; height: 72px; background: #27ae60; color: white; border-radius: 50%; font-size: 2.2rem; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.25rem; }
.success-card h2 { font-family: 'Playfair Display', serif; font-size: 1.8rem; margin-bottom: 0.75rem; color: #1a1a2e; }
.success-card p { color: #666; font-size: 1rem; line-height: 1.6; margin-bottom: 1.5rem; }
.btn-primary { padding: 0.9rem 2.5rem; background: #1a1a2e; color: #fff; border: none; border-radius: 10px; font-family: 'DM Sans', sans-serif; font-size: 1rem; font-weight: 600; cursor: pointer; }
.btn-primary:hover { background: #2c2c50; }

/* RESPONSIVE */
@media (max-width: 600px) {
  .content { padding: 1.25rem 1rem; gap: 1rem; }
  .card { padding: 1.25rem; border-radius: 12px; }
  .item-img { width: 64px; height: 64px; }
  .item-name { font-size: 0.95rem; }
  .qty-btn { width: 32px; height: 32px; font-size: 1rem; }
  .brand { font-size: 1.2rem; }
  .restaurant-name { font-size: 0.85rem; }
}

@media (max-width: 400px) {
  .menu-item { gap: 0.75rem; }
  .item-img { width: 56px; height: 56px; }
  .sold-out-label { font-size: 0.72rem; }
}
</style>
