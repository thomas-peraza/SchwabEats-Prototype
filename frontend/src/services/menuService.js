import { menuItems } from '../data/menuItems'

export async function getMenuByVendorId(vendorId) {
  const items = menuItems.filter((item) => item.vendorId === Number(vendorId))
  return Promise.resolve(items)
}