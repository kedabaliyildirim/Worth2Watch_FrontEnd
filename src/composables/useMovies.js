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
    const res = await fetch(`${import.meta.env.BASE_URL}movies.json`)
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

export function useMovie(tmdbId, mediaType) {
  loadOnce()
  return computed(() => {
    if (tmdbId == null) return null
    const idStr = String(tmdbId)
    if (mediaType) {
      const exact = movies.value.find(
        (m) => String(m.tmdbId) === idStr && m.mediaType === mediaType
      )
      if (exact) return exact
    }
    // Movies and TV shows can share TMDB ids since they're different
    // namespaces; without a hint we fall back to the first match.
    return movies.value.find((m) => String(m.tmdbId) === idStr) || null
  })
}
