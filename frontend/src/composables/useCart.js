import { computed, ref } from 'vue'

const cartItems = ref(JSON.parse(localStorage.getItem('cartItems')) || [])

function persistCart() {
  localStorage.setItem('cartItems', JSON.stringify(cartItems.value))
}

export function useCart() {
  function addToCart(item) {
    const existing = cartItems.value.find((cartItem) => cartItem.id === item.id)

    if (existing) {
      existing.quantity += 1
    } else {
      cartItems.value.push({ ...item, quantity: 1 })
    }

    persistCart()
  }

  function removeFromCart(id) {
    cartItems.value = cartItems.value.filter((item) => item.id !== id)
    persistCart()
  }

  function updateQuantity(id, quantity) {
    const item = cartItems.value.find((cartItem) => cartItem.id === id)
    if (!item) return

    if (quantity <= 0) {
      removeFromCart(id)
      return
    }

    item.quantity = quantity
    persistCart()
  }

  function clearCart() {
    cartItems.value = []
    persistCart()
  }

  const subtotal = computed(() =>
    cartItems.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
  )

  const itemCount = computed(() =>
    cartItems.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  return {
    cartItems,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    subtotal,
    itemCount
  }
}