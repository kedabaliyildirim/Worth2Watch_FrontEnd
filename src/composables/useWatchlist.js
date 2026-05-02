import { ref, computed, watch } from 'vue'

const STORAGE_KEY = 'w2w-watchlist'

function readInitial() {
  if (typeof window === 'undefined') return new Set()
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY)
    if (!raw) return new Set()
    const parsed = JSON.parse(raw)
    if (Array.isArray(parsed)) {
      return new Set(parsed.filter((x) => typeof x === 'string'))
    }
  } catch {
    // corrupt JSON
  }
  return new Set()
}

// Tek bir paylaşılan reactive watchlist seti — composable her çağrıldığında
// aynı state'i döndürür, böylece header ve liste senkron kalır.
const ids = ref(readInitial())

watch(
  ids,
  (next) => {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify([...next]))
    } catch {
      // quota / private mode — ignore
    }
  },
  { deep: true }
)

export function useWatchlist() {
  function has(id) {
    return ids.value.has(id)
  }
  function toggle(id) {
    const next = new Set(ids.value)
    if (next.has(id)) next.delete(id)
    else next.add(id)
    ids.value = next
  }
  function clear() {
    ids.value = new Set()
  }
  const count = computed(() => ids.value.size)
  return { ids, has, toggle, clear, count }
}
