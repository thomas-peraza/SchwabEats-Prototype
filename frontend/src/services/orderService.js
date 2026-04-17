import { orders } from '../data/orders'

export async function getOrders() {
  return Promise.resolve(orders)
}

export async function submitOrder(orderPayload) {
  console.log('Mock order submitted:', orderPayload)
  return Promise.resolve({
    success: true,
    orderNumber: Math.floor(Math.random() * 90000) + 10000
  })
}