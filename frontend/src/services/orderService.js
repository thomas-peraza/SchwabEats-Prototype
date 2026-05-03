import { orders } from '../data/orders'
import { post } from './api'

export async function getOrders() {
  return Promise.resolve(orders)
}

export async function submitOrder(orderPayload) {
  return post('/api/orders/place', orderPayload)
}

export async function quoteOrder(orderPayload) {
  return post('/api/orders/quote', orderPayload)
}