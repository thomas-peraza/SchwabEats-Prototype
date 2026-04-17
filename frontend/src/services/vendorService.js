import { vendors } from '../data/vendors'

export async function getVendors() {
  return Promise.resolve(vendors)
}

export async function getVendorById(id) {
  const vendor = vendors.find((item) => item.id === Number(id))
  return Promise.resolve(vendor)
}