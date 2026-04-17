<template>
  <span
    class="px-3 py-1 rounded-full text-xs font-semibold"
    :class="badgeClass"
  >
    {{ status }}
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true
  }
})

const badgeClass = computed(() => {
  switch (props.status.toLowerCase()) {
    case 'accepted':
      return 'bg-blue-100 text-blue-700'
    case 'preparing':
      return 'bg-yellow-100 text-yellow-700'
    case 'ready':
      return 'bg-green-100 text-green-700'
    case 'completed':
      return 'bg-slate-200 text-slate-700'
    default:
      return 'bg-slate-100 text-slate-700'
  }
})
</script>