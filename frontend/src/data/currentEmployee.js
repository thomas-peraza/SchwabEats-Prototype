export const currentEmployee = {
  id: 'emp-1001',
  campus_id: 'dallas-park-cities',
  role: 'full-time',
  is_on_leave: false,
  is_terminated: false,
  is_eligible: true,
  orders_today: 0,
  dietary_flags: [],
  order_history: [],
  timezone: 'America/Chicago'
}

export function getCurrentEmployee() {
  try {
    const saved = localStorage.getItem('schwabeatsCurrentEmployee')
    if (!saved) return currentEmployee

    return {
      ...currentEmployee,
      ...JSON.parse(saved)
    }
  } catch {
    return currentEmployee
  }
}

export function saveCurrentEmployee(employee) {
  localStorage.setItem('schwabeatsCurrentEmployee', JSON.stringify(employee))
}