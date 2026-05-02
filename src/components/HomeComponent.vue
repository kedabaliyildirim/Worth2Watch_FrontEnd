<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import {
  Search,
  ArrowUpDown,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Bookmark,
  Sparkles,
  X,
  Filter as FilterIcon,
  Film,
  Tv,
  Layers,
} from 'lucide-vue-next'
import MovieListItem from './MovieListItem.vue'
import SkeletonRow from './SkeletonRow.vue'
import { useMovies } from '../composables/useMovies.js'
import { useWatchlist } from '../composables/useWatchlist.js'

const router = useRouter()
const { movies, loading, error } = useMovies()
const watchlist = useWatchlist()

const searchTerm = ref('')
const sortOption = ref('imdbRating')
const sortOrder = ref('desc')
const onlyWatchlist = ref(false)
const mediaType = ref('all') // 'all' | 'movie' | 'tv'
const selectedGenres = ref([])
const selectedProviders = ref([])
const yearFrom = ref(null)
const yearTo = ref(null)
const page = ref(1)
const pageSize = 30
const sortMenuOpen = ref(false)

const SORT_OPTIONS = [
  { id: 'imdbRating', label: 'IMDB' },
  { id: 'tmdbRating', label: 'TMDB' },
  { id: 'releaseDate', label: 'Yayın Tarihi' },
  { id: 'popularity', label: 'Popülerlik' },
  { id: 'title', label: 'Alfabetik' },
]

const allGenres = computed(() => {
  const set = new Set()
  for (const m of movies.value) {
    for (const g of m.genres || []) set.add(g)
  }
  return [...set].sort()
})

// Provider chip row için: TR'de en çok film barındıran ilk 12 platformu
// göster. Aksi halde TMDB'nin 100+ niche channel'ı liste'yi kirletiyor
// ("A&E Crime Central", "ALLBLK Amazon channel" vs.).
const allProviders = computed(() => {
  const counts = new Map()
  const meta = new Map()
  for (const m of movies.value) {
    for (const p of m.providers || []) {
      counts.set(p.id, (counts.get(p.id) || 0) + 1)
      if (!meta.has(p.id)) meta.set(p.id, p)
    }
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 12)
    .map(([id]) => meta.get(id))
})

const yearBounds = computed(() => {
  let min = null
  let max = null
  for (const m of movies.value) {
    const y = parseInt(m.year, 10)
    if (Number.isNaN(y)) continue
    if (min === null || y < min) min = y
    if (max === null || y > max) max = y
  }
  return { min, max }
})

const filtered = computed(() => {
  if (!movies.value.length) return []
  let res = movies.value
  if (mediaType.value !== 'all') {
    res = res.filter((m) => m.mediaType === mediaType.value)
  }
  const term = searchTerm.value.trim().toLowerCase()
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
  if (yearFrom.value) {
    res = res.filter((m) => parseInt(m.year, 10) >= yearFrom.value)
  }
  if (yearTo.value) {
    res = res.filter((m) => parseInt(m.year, 10) <= yearTo.value)
  }
  if (onlyWatchlist.value) {
    res = res.filter((m) =>
      watchlist.has(`${m.mediaType}-${m.tmdbId}`)
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
    !!searchTerm.value ||
    onlyWatchlist.value ||
    mediaType.value !== 'all' ||
    selectedGenres.value.length > 0 ||
    selectedProviders.value.length > 0 ||
    yearFrom.value !== null ||
    yearTo.value !== null
)

function selectMovie(movie) {
  router.push({ name: 'movie', params: { id: movie.tmdbId, mediaType: movie.mediaType } })
}

function clearFilters() {
  searchTerm.value = ''
  onlyWatchlist.value = false
  mediaType.value = 'all'
  selectedGenres.value = []
  selectedProviders.value = []
  yearFrom.value = null
  yearTo.value = null
}

function setMediaType(t) {
  mediaType.value = t
  page.value = 1
}

function toggleGenre(g) {
  const i = selectedGenres.value.indexOf(g)
  if (i >= 0) selectedGenres.value.splice(i, 1)
  else selectedGenres.value.push(g)
  page.value = 1
}

function toggleProvider(id) {
  const i = selectedProviders.value.indexOf(id)
  if (i >= 0) selectedProviders.value.splice(i, 1)
  else selectedProviders.value.push(id)
  page.value = 1
}

function onClickOutside(e) {
  if (!e.target.closest('[data-sort-menu]')) sortMenuOpen.value = false
}
onMounted(() => document.addEventListener('click', onClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', onClickOutside))
</script>

<template>
  <main class="max-w-7xl mx-auto px-4 py-8">
    <!-- Search + sort row -->
    <div class="mb-4 flex flex-wrap items-center gap-3">
      <div class="relative flex-1 min-w-[260px] max-w-xl">
        <Search
          :size="16"
          class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none"
        />
        <input
          v-model="searchTerm"
          type="text"
          placeholder="Film veya tür ara..."
          class="w-full pl-9 pr-3 py-2.5 bg-slate-800/40 border border-slate-700/50 focus:border-indigo-500/60 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 text-slate-200 placeholder:text-slate-500 rounded-lg text-sm transition-colors"
          @input="page = 1"
        />
      </div>

      <div class="relative" data-sort-menu>
        <button
          type="button"
          class="flex items-center gap-2 px-3.5 py-2.5 bg-slate-800/40 border border-slate-700/50 hover:border-indigo-500/50 rounded-lg text-sm font-semibold text-slate-200 transition-colors"
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
            ? 'Artan, tıkla azalan yap'
            : 'Azalan, tıkla artan yap'
        "
        class="flex items-center justify-center w-10 h-10 bg-slate-800/40 border border-slate-700/50 hover:border-indigo-500/50 rounded-lg text-indigo-400 hover:text-indigo-300 transition-colors"
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

      <div
        class="flex items-center gap-1 p-1 bg-slate-800/40 border border-slate-700/40 rounded-lg"
      >
        <button
          type="button"
          :aria-pressed="mediaType === 'all'"
          class="px-3 py-1.5 rounded-md text-xs font-bold transition-colors"
          :class="
            mediaType === 'all'
              ? 'bg-indigo-500 text-white shadow-md shadow-indigo-500/30'
              : 'text-slate-400 hover:text-white'
          "
          @click="setMediaType('all')"
        >
          Tümü
        </button>
        <button
          type="button"
          :aria-pressed="mediaType === 'movie'"
          class="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-bold transition-colors"
          :class="
            mediaType === 'movie'
              ? 'bg-cyan-500 text-slate-900 shadow-md shadow-cyan-500/30'
              : 'text-slate-400 hover:text-white'
          "
          @click="setMediaType('movie')"
        >
          <Film :size="12" /> Film
        </button>
        <button
          type="button"
          :aria-pressed="mediaType === 'tv'"
          class="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-bold transition-colors"
          :class="
            mediaType === 'tv'
              ? 'bg-violet-500 text-white shadow-md shadow-violet-500/30'
              : 'text-slate-400 hover:text-white'
          "
          @click="setMediaType('tv')"
        >
          <Tv :size="12" /> Dizi
        </button>
      </div>

      <button
        v-if="watchlist.count.value > 0"
        type="button"
        :aria-pressed="onlyWatchlist"
        class="flex items-center gap-2 px-3.5 py-2.5 rounded-lg text-sm font-bold border transition-all"
        :class="
          onlyWatchlist
            ? 'bg-indigo-500 text-white border-indigo-400 shadow-[0_0_18px_rgba(99,102,241,0.35)]'
            : 'bg-slate-800/40 text-slate-300 border-slate-700/60 hover:border-indigo-500/50 hover:text-white'
        "
        @click="onlyWatchlist = !onlyWatchlist; page = 1"
      >
        <Bookmark :size="14" :fill="onlyWatchlist ? 'currentColor' : 'none'" />
        Listem
        <span
          class="text-[10px] font-mono"
          :class="onlyWatchlist ? 'text-white/80' : 'text-slate-500'"
        >
          {{ watchlist.count.value }}
        </span>
      </button>

      <button
        v-if="hasActiveFilters"
        type="button"
        class="text-xs font-semibold text-slate-400 hover:text-white flex items-center gap-1 transition-colors ml-auto"
        @click="clearFilters"
      >
        <X :size="12" /> Filtreleri sıfırla
      </button>
    </div>

    <!-- Filter row: provider chips + year range -->
    <div class="mb-4 space-y-3">
      <div v-if="allProviders.length" class="flex items-center gap-3">
        <span
          class="text-[10px] font-bold uppercase tracking-widest text-slate-500 flex items-center gap-1.5 flex-shrink-0"
        >
          <FilterIcon :size="12" /> Platform
        </span>
        <div class="no-scrollbar flex-1 flex items-center gap-2 overflow-x-auto py-1">
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

      <div v-if="allGenres.length" class="flex items-center gap-3">
        <span
          class="text-[10px] font-bold uppercase tracking-widest text-slate-500 flex-shrink-0"
        >
          Tür
        </span>
        <div class="no-scrollbar flex-1 flex items-center gap-2 overflow-x-auto py-1">
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
            {{ g }}
          </button>
        </div>
      </div>

      <div
        v-if="yearBounds.min && yearBounds.max"
        class="flex items-center gap-3"
      >
        <span
          class="text-[10px] font-bold uppercase tracking-widest text-slate-500 flex-shrink-0"
        >
          Yıl
        </span>
        <div class="flex items-center gap-2">
          <input
            v-model.number="yearFrom"
            type="number"
            :min="yearBounds.min"
            :max="yearBounds.max"
            :placeholder="yearBounds.min"
            class="w-20 px-2 py-1 bg-slate-800/40 border border-slate-700/60 focus:border-indigo-500/60 focus:outline-none rounded-md text-xs text-slate-200 placeholder:text-slate-500"
            @input="page = 1"
          />
          <span class="text-slate-500 text-xs">→</span>
          <input
            v-model.number="yearTo"
            type="number"
            :min="yearBounds.min"
            :max="yearBounds.max"
            :placeholder="yearBounds.max"
            class="w-20 px-2 py-1 bg-slate-800/40 border border-slate-700/60 focus:border-indigo-500/60 focus:outline-none rounded-md text-xs text-slate-200 placeholder:text-slate-500"
            @input="page = 1"
          />
        </div>
      </div>
    </div>

    <div class="flex justify-between items-end mb-4 px-1">
      <h2 class="text-2xl font-bold text-white flex items-center gap-2">
        <Sparkles class="text-indigo-400" :size="22" />
        Keşfet
      </h2>
      <span class="text-xs text-slate-500 font-mono">
        {{ filtered.length }} sonuç
      </span>
    </div>

    <div
      class="hidden lg:flex items-center gap-8 px-4 py-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest border-b border-slate-800/50 mb-2 mr-4"
    >
      <div class="w-8 text-center">#</div>
      <div class="w-16 flex-shrink-0"></div>
      <div class="flex-1">Film / Dizi</div>
      <div class="flex items-center gap-8">
        <div class="w-14 text-center">Worth</div>
        <div class="w-14 text-center">TMDB</div>
        <div class="w-32 text-center">Platform / Bölümler</div>
      </div>
    </div>

    <div class="space-y-2">
      <template v-if="loading">
        <SkeletonRow v-for="i in 8" :key="i" />
      </template>

      <div
        v-else-if="error"
        class="text-center py-16 px-6 bg-red-500/10 rounded-2xl border border-red-500/30 border-dashed"
      >
        <p class="text-red-300 font-bold text-lg mb-1">Katalog yüklenemedi</p>
        <p class="text-slate-500 text-sm mb-5">
          movies.json çekilemedi — public/movies.json'ı build_catalog.py ile
          oluştur.
        </p>
      </div>

      <template v-else-if="paged.length > 0">
        <MovieListItem
          v-for="(m, i) in paged"
          :key="m.tmdbId"
          :movie="m"
          :index="(page - 1) * pageSize + i + 1"
          :in-watchlist="watchlist.has(m.tmdbId)"
          @select="selectMovie"
          @toggle-watchlist="watchlist.toggle"
        />
      </template>

      <div
        v-else
        class="text-center py-16 px-6 bg-slate-800/20 rounded-2xl border border-slate-700/30 border-dashed"
      >
        <p class="text-slate-300 font-bold text-lg mb-1">Hiç sonuç yok</p>
        <p class="text-slate-500 text-sm mb-5">
          Filtreleri gevşet — bu kombinasyonda film bulunmuyor.
        </p>
        <button
          type="button"
          class="inline-flex items-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-bold rounded-lg transition-colors shadow-lg shadow-indigo-500/20"
          @click="clearFilters"
        >
          Filtreleri sıfırla
        </button>
      </div>
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
        <ChevronLeft :size="14" /> Önceki
      </button>
      <span class="px-4 text-sm font-mono text-slate-400">
        Sayfa <span class="text-white font-bold">{{ page }}</span> /
        {{ totalPages }}
      </span>
      <button
        type="button"
        class="flex items-center gap-1 px-3 py-2 bg-slate-800/40 border border-slate-700/50 hover:border-indigo-500/50 rounded-lg text-sm font-semibold text-slate-300 hover:text-white transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
        :disabled="page >= totalPages"
        @click="page = Math.min(totalPages, page + 1)"
      >
        Sonraki <ChevronRight :size="14" />
      </button>
    </div>
  </main>
</template>
