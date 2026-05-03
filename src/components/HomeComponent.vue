<script setup>
import { computed, ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  ArrowUpDown,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  X,
  Film,
  Tv,
} from 'lucide-vue-next'
import MovieCard from './MovieCard.vue'
import { useMovies } from '../composables/useMovies.js'
import { useGlobalSearch } from '../composables/useGlobalSearch.js'
import { translateGenre } from '../composables/useGenreMap.js'

const router = useRouter()
const { movies, loading, error } = useMovies()
const search = useGlobalSearch()

const sortOption = ref('worthScore')
const sortOrder = ref('desc')
const mediaType = ref('all') // 'all' | 'movie' | 'tv'
const selectedGenres = ref([])
const selectedProviders = ref([])
const page = ref(1)
const pageSize = 36
const sortMenuOpen = ref(false)

const SORT_OPTIONS = [
  { id: 'worthScore', label: 'Worth Score' },
  { id: 'imdbRating', label: 'IMDb' },
  { id: 'tmdbRating', label: 'TMDB' },
  { id: 'releaseDate', label: 'Release Date' },
  { id: 'popularity', label: 'Popularity' },
  { id: 'title', label: 'Alphabetical' },
]

// Curated short list of major streaming services. The TMDB watch/providers
// API returns 100+ niche channels (Plex, Tubi, Hoopla, Kanopy, regional
// Amazon channel-of-channels) which clutter the filter strip. Stick to
// services Turkish viewers actually use.
const MAJOR_PROVIDER_IDS = new Set([
  8, // Netflix
  9, // Prime Video
  337, // Disney Plus
  384, // HBO Max
  350, // Apple TV+
  283, // Crunchyroll
  531, // Paramount+
  386, // Peacock
  192, // YouTube Premium
])

const allGenres = computed(() => {
  const set = new Set()
  for (const m of movies.value) {
    for (const g of m.genres || []) set.add(g)
  }
  return [...set].sort()
})

const allProviders = computed(() => {
  const map = new Map()
  for (const m of movies.value) {
    for (const p of m.providers || []) {
      if (!MAJOR_PROVIDER_IDS.has(p.id)) continue
      if (!map.has(p.id)) map.set(p.id, p)
    }
  }
  return [...map.values()].sort((a, b) => a.name.localeCompare(b.name))
})

const filtered = computed(() => {
  if (!movies.value.length) return []
  let res = movies.value
  if (mediaType.value !== 'all') {
    res = res.filter((m) => m.mediaType === mediaType.value)
  }
  const term = search.term.value.trim().toLowerCase()
  if (term) {
    res = res.filter(
      (m) =>
        m.title?.toLowerCase().includes(term) ||
        m.originalTitle?.toLowerCase().includes(term) ||
        (m.genres || []).some((g) => g.toLowerCase().includes(term))
    )
  }
  if (selectedGenres.value.length) {
    res = res.filter((m) =>
      selectedGenres.value.every((g) => (m.genres || []).includes(g))
    )
  }
  if (selectedProviders.value.length) {
    const want = new Set(selectedProviders.value)
    res = res.filter((m) =>
      (m.providers || []).some((p) => want.has(p.id))
    )
  }
  const dir = sortOrder.value === 'asc' ? 1 : -1
  res = [...res].sort((a, b) => {
    const av = a[sortOption.value]
    const bv = b[sortOption.value]
    if (av == null && bv == null) return 0
    if (av == null) return 1
    if (bv == null) return -1
    if (typeof av === 'string') return av.localeCompare(bv) * dir
    return (av - bv) * dir
  })
  return res
})

const totalPages = computed(() =>
  Math.max(1, Math.ceil(filtered.value.length / pageSize))
)

const paged = computed(() =>
  filtered.value.slice((page.value - 1) * pageSize, page.value * pageSize)
)

const sortLabel = computed(
  () => SORT_OPTIONS.find((o) => o.id === sortOption.value)?.label || ''
)

const hasActiveFilters = computed(
  () =>
    !!search.term.value ||
    mediaType.value !== 'all' ||
    selectedGenres.value.length > 0 ||
    selectedProviders.value.length > 0
)

watch(
  [search.term, mediaType, selectedGenres, selectedProviders, sortOption, sortOrder],
  () => {
    page.value = 1
  }
)

function selectMovie(movie) {
  router.push({
    name: 'movie',
    params: { id: movie.tmdbId, mediaType: movie.mediaType },
  })
}

function clearFilters() {
  search.setTerm('')
  mediaType.value = 'all'
  selectedGenres.value = []
  selectedProviders.value = []
}

function setMediaType(t) {
  mediaType.value = t
}

function toggleGenre(g) {
  const i = selectedGenres.value.indexOf(g)
  if (i >= 0) selectedGenres.value.splice(i, 1)
  else selectedGenres.value.push(g)
}

function toggleProvider(id) {
  const i = selectedProviders.value.indexOf(id)
  if (i >= 0) selectedProviders.value.splice(i, 1)
  else selectedProviders.value.push(id)
}

function onClickOutside(e) {
  if (!e.target.closest('[data-sort-menu]')) sortMenuOpen.value = false
}
onMounted(() => document.addEventListener('click', onClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', onClickOutside))
</script>

<template>
  <main class="max-w-7xl mx-auto px-4 py-8">
    <!-- Top filter row: media-type segmented on the left, sort on the right -->
    <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
      <!-- Media-type segmented (primary action — left) -->
      <div
        class="flex items-center gap-1 p-1 bg-slate-800/40 border border-slate-700/40 rounded-lg"
      >
        <button
          type="button"
          :aria-pressed="mediaType === 'all'"
          class="px-4 py-1.5 rounded-md text-xs font-bold transition-colors"
          :class="
            mediaType === 'all'
              ? 'bg-indigo-500 text-white shadow-md shadow-indigo-500/30'
              : 'text-slate-400 hover:text-white'
          "
          @click="setMediaType('all')"
        >
          All
        </button>
        <button
          type="button"
          :aria-pressed="mediaType === 'movie'"
          class="flex items-center gap-1.5 px-4 py-1.5 rounded-md text-xs font-bold transition-colors"
          :class="
            mediaType === 'movie'
              ? 'bg-cyan-500 text-slate-900 shadow-md shadow-cyan-500/30'
              : 'text-slate-400 hover:text-white'
          "
          @click="setMediaType('movie')"
        >
          <Film :size="12" /> Movies
        </button>
        <button
          type="button"
          :aria-pressed="mediaType === 'tv'"
          class="flex items-center gap-1.5 px-4 py-1.5 rounded-md text-xs font-bold transition-colors"
          :class="
            mediaType === 'tv'
              ? 'bg-violet-500 text-white shadow-md shadow-violet-500/30'
              : 'text-slate-400 hover:text-white'
          "
          @click="setMediaType('tv')"
        >
          <Tv :size="12" /> Series
        </button>
      </div>

      <!-- Right cluster: reset (when active) + sort -->
      <div class="flex items-center gap-2">
        <button
          v-if="hasActiveFilters"
          type="button"
          class="text-xs font-semibold text-slate-400 hover:text-white flex items-center gap-1 transition-colors mr-1"
          @click="clearFilters"
        >
          <X :size="12" /> Reset
        </button>

        <span class="text-[10px] font-bold uppercase tracking-widest text-slate-500 mr-1">
          Sort
        </span>

        <div class="relative" data-sort-menu>
          <button
            type="button"
            class="flex items-center gap-2 px-3 py-2 bg-slate-800/40 border border-slate-700/50 hover:border-indigo-500/50 rounded-l-lg text-sm font-semibold text-slate-200 transition-colors"
            @click="sortMenuOpen = !sortMenuOpen"
          >
            <ArrowUpDown :size="14" class="text-indigo-400" />
            {{ sortLabel }}
            <ChevronDown
              :size="14"
              :class="
                sortMenuOpen
                  ? 'rotate-180 transition-transform'
                  : 'transition-transform'
              "
            />
          </button>
          <div
            v-if="sortMenuOpen"
            class="absolute right-0 mt-2 w-52 bg-slate-900 border border-slate-700/60 rounded-xl shadow-2xl overflow-hidden z-20 animate-fade-in"
          >
            <button
              v-for="opt in SORT_OPTIONS"
              :key="opt.id"
              type="button"
              class="w-full text-left px-4 py-2.5 text-sm font-semibold transition-colors"
              :class="
                sortOption === opt.id
                  ? 'bg-indigo-500/20 text-indigo-300'
                  : 'text-slate-300 hover:bg-slate-800'
              "
              @click="sortOption = opt.id; sortMenuOpen = false"
            >
              {{ opt.label }}
            </button>
          </div>
        </div>

        <button
          type="button"
          :aria-label="
            sortOrder === 'asc'
              ? 'Ascending — click to flip to descending'
              : 'Descending — click to flip to ascending'
          "
          class="flex items-center justify-center w-10 h-10 bg-slate-800/40 border border-l-0 border-slate-700/50 hover:border-indigo-500/50 rounded-r-lg text-indigo-400 hover:text-indigo-300 transition-colors"
          @click="sortOrder = sortOrder === 'asc' ? 'desc' : 'asc'"
        >
          <ChevronDown
            :size="18"
            :class="
              sortOrder === 'asc'
                ? 'rotate-180 transition-transform'
                : 'transition-transform'
            "
          />
        </button>
      </div>
    </div>

    <!-- Provider + Genre chip rows -->
    <div class="mb-6 space-y-3">
      <div v-if="allProviders.length" class="flex items-center gap-3 flex-wrap">
        <span class="text-[10px] font-bold uppercase tracking-widest text-slate-500 flex-shrink-0">
          Platform
        </span>
        <div class="flex items-center gap-2 flex-wrap">
          <button
            v-for="p in allProviders"
            :key="p.id"
            type="button"
            :aria-pressed="selectedProviders.includes(p.id)"
            class="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border transition-all whitespace-nowrap"
            :class="
              selectedProviders.includes(p.id)
                ? 'bg-indigo-500 text-white border-indigo-400 shadow-[0_0_12px_rgba(99,102,241,0.35)]'
                : 'bg-slate-800/40 text-slate-300 border-slate-700/60 hover:border-indigo-500/50 hover:text-white'
            "
            @click="toggleProvider(p.id)"
          >
            <img
              :src="`https://image.tmdb.org/t/p/original${p.logo}`"
              :alt="p.name"
              class="w-4 h-4 rounded object-cover"
            />
            {{ p.name }}
          </button>
        </div>
      </div>

      <div v-if="allGenres.length" class="flex items-center gap-3 flex-wrap">
        <span class="text-[10px] font-bold uppercase tracking-widest text-slate-500 flex-shrink-0">
          Genre
        </span>
        <div class="flex items-center gap-2 flex-wrap">
          <button
            v-for="g in allGenres"
            :key="g"
            type="button"
            :aria-pressed="selectedGenres.includes(g)"
            class="px-2.5 py-1 rounded-full text-xs font-semibold border transition-all whitespace-nowrap"
            :class="
              selectedGenres.includes(g)
                ? 'bg-indigo-500 text-white border-indigo-400'
                : 'bg-slate-800/40 text-slate-300 border-slate-700/60 hover:border-indigo-500/50 hover:text-white'
            "
            @click="toggleGenre(g)"
          >
            {{ translateGenre(g) }}
          </button>
        </div>
      </div>
    </div>

    <!-- Header band -->
    <div class="flex justify-between items-end mb-4 px-1">
      <h2 class="text-2xl font-bold text-white flex items-center gap-2">
        <Sparkles class="text-indigo-400" :size="22" />
        Discover
      </h2>
      <span class="text-xs text-slate-500 font-mono">
        {{ filtered.length }} results
      </span>
    </div>

    <!-- Card grid -->
    <template v-if="loading">
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <div
          v-for="i in 12"
          :key="i"
          class="aspect-[2/3] rounded-xl bg-slate-800/40 border border-slate-700/40 animate-pulse"
        />
      </div>
    </template>

    <div
      v-else-if="error"
      class="text-center py-16 px-6 bg-red-500/10 rounded-2xl border border-red-500/30 border-dashed"
    >
      <p class="text-red-300 font-bold text-lg mb-1">Catalog failed to load</p>
      <p class="text-slate-500 text-sm">
        movies.json couldn't be fetched — rebuild it via build_catalog.py.
      </p>
    </div>

    <template v-else-if="paged.length > 0">
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <MovieCard
          v-for="m in paged"
          :key="`${m.mediaType}-${m.tmdbId}`"
          :movie="m"
          @select="selectMovie"
        />
      </div>
    </template>

    <div
      v-else
      class="text-center py-16 px-6 bg-slate-800/20 rounded-2xl border border-slate-700/30 border-dashed"
    >
      <p class="text-slate-300 font-bold text-lg mb-1">No results</p>
      <p class="text-slate-500 text-sm mb-5">
        Loosen the filters — nothing matched this combination.
      </p>
      <button
        type="button"
        class="inline-flex items-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-bold rounded-lg transition-colors shadow-lg shadow-indigo-500/20"
        @click="clearFilters"
      >
        Reset filters
      </button>
    </div>

    <div
      v-if="totalPages > 1"
      class="flex justify-center items-center gap-2 mt-8"
    >
      <button
        type="button"
        class="flex items-center gap-1 px-3 py-2 bg-slate-800/40 border border-slate-700/50 hover:border-indigo-500/50 rounded-lg text-sm font-semibold text-slate-300 hover:text-white transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
        :disabled="page <= 1"
        @click="page = Math.max(1, page - 1)"
      >
        <ChevronLeft :size="14" /> Previous
      </button>
      <span class="px-4 text-sm font-mono text-slate-400">
        Page <span class="text-white font-bold">{{ page }}</span> /
        {{ totalPages }}
      </span>
      <button
        type="button"
        class="flex items-center gap-1 px-3 py-2 bg-slate-800/40 border border-slate-700/50 hover:border-indigo-500/50 rounded-lg text-sm font-semibold text-slate-300 hover:text-white transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
        :disabled="page >= totalPages"
        @click="page = Math.min(totalPages, page + 1)"
      >
        Next <ChevronRight :size="14" />
      </button>
    </div>
  </main>
</template>
