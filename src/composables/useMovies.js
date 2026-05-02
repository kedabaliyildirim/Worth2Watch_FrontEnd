import { ref, computed, readonly } from 'vue'

// Tek bir paylaşılan reactive cache. Composable her çağrıldığında aynı
// state'i döndürür — fetch sadece ilk çağrıda çalışır.
const movies = ref([])
const loading = ref(false)
const error = ref(null)
let bootstrapped = false

async function loadOnce() {
  if (bootstrapped) return
  bootstrapped = true
  loading.value = true
  try {
    const res = await fetch(`${import.meta.env.BASE_URL}movies.json`, {
      cache: 'force-cache',
    })
    if (!res.ok) throw new Error(`movies.json: ${res.status}`)
    movies.value = await res.json()
  } catch (err) {
    error.value = err
    movies.value = []
  } finally {
    loading.value = false
  }
}

export function useMovies() {
  loadOnce()
  return {
    movies: readonly(movies),
    loading: readonly(loading),
    error: readonly(error),
  }
}

export function useMovie(tmdbIdOrTitle) {
  loadOnce()
  return computed(() => {
    if (!tmdbIdOrTitle) return null
    const needle = String(tmdbIdOrTitle).toLowerCase()
    return (
      movies.value.find(
        (m) => String(m.tmdbId) === String(tmdbIdOrTitle)
      ) ||
      movies.value.find((m) => m.title?.toLowerCase() === needle) ||
      null
    )
  })
}
