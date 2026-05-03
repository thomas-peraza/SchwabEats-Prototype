import { menuItems } from '../data/menuItems'
import { vendors } from '../data/vendors'
import { getCurrentEmployee } from '../data/currentEmployee'
import { post } from './api'

function buildVendorPayload(vendor) {
  return {
    id: String(vendor.id),
    name: vendor.name,
    contract_status: 'Active',
    accepting_orders: true,
    delivery_zones: [getCurrentEmployee().campus_id],
    menu_items: menuItems
      .filter((item) => item.vendorId === Number(vendor.id))
      .map((item) => ({
        id: String(item.id),
        vendor_id: String(vendor.id),
        name: item.name,
        allergen_codes: [],
        restriction_codes: [],
        cuisine_type: vendor.cuisine,
        is_available: true
      })),
    performance_score: 0.72,
    average_rating: vendor.rating,
    metadata: {
      image: vendor.image,
      deliveryTime: vendor.deliveryTime,
      description: vendor.description
    }
  }
}

export async function getRecommendedVendors() {
  const employee = getCurrentEmployee()
  const payload = {
    employee,
    vendors: vendors.map(buildVendorPayload),
    request_time_local: new Date().toISOString(),
    top_n: 3,
    campus_popularity: {}
  }

  try {
    const response = await post('/api/recommendations', payload)
    const rankedVendorIds = (response.recommendations || []).map((item) => Number(item.vendor_id))

    return rankedVendorIds
      .map((vendorId) => vendors.find((vendor) => vendor.id === vendorId))
      .filter(Boolean)
  } catch {
    return vendors.slice(0, 3)
  }
}

export async function getRankedVendorCatalog() {
  const recommended = await getRecommendedVendors()
  const recommendedIds = new Set(recommended.map((vendor) => vendor.id))
  const remaining = vendors.filter((vendor) => !recommendedIds.has(vendor.id))

  return [...recommended, ...remaining]
}

export function buildBackendVendor(vendorId) {
  const vendor = vendors.find((item) => item.id === Number(vendorId))
  if (!vendor) return null

  return buildVendorPayload(vendor)
}