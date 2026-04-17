import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import EmployeeDashboardView from '../views/EmployeeDashboardView.vue'
import VendorsView from '../views/VendorsView.vue'
import MenuView from '../views/MenuView.vue'
import CartView from '../views/CartView.vue'
import CheckoutView from '../views/CheckoutView.vue'
import OrderConfirmationView from '../views/OrderConfirmationView.vue'
import VendorDashboardView from '../views/VendorDashboardView.vue'
import VendorOrdersView from '../views/VendorOrdersView.vue'

const routes = [
  { path: '/', name: 'login', component: LoginView },
  { path: '/employee', name: 'employee-dashboard', component: EmployeeDashboardView },
  { path: '/vendors', name: 'vendors', component: VendorsView },
  { path: '/vendors/:id/menu', name: 'menu', component: MenuView, props: true },
  { path: '/cart', name: 'cart', component: CartView },
  { path: '/checkout', name: 'checkout', component: CheckoutView },
  { path: '/order-confirmation', name: 'order-confirmation', component: OrderConfirmationView },
  { path: '/vendor-dashboard', name: 'vendor-dashboard', component: VendorDashboardView },
  { path: '/vendor-orders', name: 'vendor-orders', component: VendorOrdersView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router