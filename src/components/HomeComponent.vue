<script setup>
import { computed, ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useStore } from 'vuex'
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
} from 'lucide-vue-next'
import MovieListItem from './MovieListItem.vue'
import SkeletonRow from './SkeletonRow.vue'
import { useWatchlist } from '../composables/useWatchlist.js'

const store = useStore()
const router = useRouter()
const watchlist = useWatchlist()

const searchTerm = ref('')
const sortOption = ref('imdbRating')
const sortOrder = ref('desc')
const onlyWatchlist = ref(false)
const page = ref(1)
const pageSize = 20
const sortMenuOpen = ref(false)

const SORT_OPTIONS = [
  { id: 'imdbRating', label: 'IMDB' },
  { id: 'tmdbRating', label: 'TMDB' },
  { id: 'rottenTomatoesRating', label: 'Rotten Tomatoes' },
  { id: 'movieReleaseDate', label: 'Yayın Tarihi' },
  { id: 'movieName', label: 'Alfabetik' },
]

const movies = computed(() => store.state.movieData ?? [])
const loading = computed(() => !movies.value || movies.value.length === 0)

function fetchPage(p) {
  store.dispatch('getMovieData', {
    page: p,
    page_size: pageSize,
    sort_by: sortOption.value,
    sort_order: sortOrder.value === 'asc' ? 1 : -1,
  })
}

onMounted(() => fetchPage(page.value))

watch([page, sortOption, sortOrder], () => {
  fetchPage(page.value)
})

const filtered = computed(() => {
  let res = [...movies.value]
  const term = searchTerm.value.trim().toLowerCase()
  if (term) {
    res = res.filter(
      (m) =>
        m.movieName?.toLowerCase().includes(term) ||
        (m.movieGenre || '').toLowerCase().includes(term)
    )
  }
  if (onlyWatchlist.value) {
    res = res.filter((m) => watchlist.has(m.movieName))
  }
  res.sort((a, b) => {
    const dir = sortOrder.value === 'asc' ? 1 : -1
    const av = a[sortOption.value] ?? 0
    const bv = b[sortOption.value] ?? 0
    if (typeof av === 'string') return av.localeCompare(bv) * dir
    return (av - bv) * dir
  })
  return res
})

const totalPages = computed(() => Math.max(1, store.state.totalPageCount || 1))

const sortLabel = computed(
  () => SORT_OPTIONS.find((o) => o.id === sortOption.value)?.label || ''
)

function selectMovie(movie) {
  router.push({ name: 'movie', params: { id: movie.movieName } })
}

function clearFilters() {
  searchTerm.value = ''
  onlyWatchlist.value = false
}

function onClickOutside(e) {
  if (!e.target.closest('[data-sort-menu]')) sortMenuOpen.value = false
}
onMounted(() => document.addEventListener('click', onClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', onClickOutside))
</script>

<template>
  <main class="max-w-7xl mx-auto px-4 py-8">
    <div class="mb-6 flex flex-wrap items-center gap-3">
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
            :class="sortMenuOpen ? 'rotate-180 transition-transform' : 'transition-transform'"
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
          :class="sortOrder === 'asc' ? 'rotate-180 transition-transform' : 'transition-transform'"
        />
      </button>

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
        @click="onlyWatchlist = !onlyWatchlist"
      >
        <Bookmark :size="14" :fill="onlyWatchlist ? 'currentColor' : 'none'" />
        İzleme listem
        <span
          class="text-[10px] font-mono"
          :class="onlyWatchlist ? 'text-white/80' : 'text-slate-500'"
        >
          {{ watchlist.count.value }}
        </span>
      </button>

      <button
        v-if="searchTerm || onlyWatchlist"
        type="button"
        class="text-xs font-semibold text-slate-400 hover:text-white flex items-center gap-1 transition-colors ml-auto"
        @click="clearFilters"
      >
        <X :size="12" /> Filtreleri sıfırla
      </button>
    </div>

    <div class="flex justify-between items-end mb-4 px-1">
      <h2 class="text-2xl font-bold text-white flex items-center gap-2">
        <Sparkles class="text-indigo-400" :size="22" />
        İzlenecek Filmler
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
      <div class="flex-1">Film</div>
      <div class="flex items-center gap-8">
        <div class="w-14 text-center">TMDB</div>
        <div class="w-14 text-center">RT</div>
        <div class="w-32 text-center">Platform</div>
      </div>
    </div>

    <div class="space-y-2">
      <template v-if="loading">
        <SkeletonRow v-for="i in 5" :key="i" />
      </template>

      <template v-else-if="filtered.length > 0">
        <MovieListItem
          v-for="(m, i) in filtered"
          :key="m.movieName"
          :movie="m"
          :index="(page - 1) * pageSize + i + 1"
          :in-watchlist="watchlist.has(m.movieName)"
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
          {{
            searchTerm.trim()
              ? `"${searchTerm}" için film bulunamadı.`
              : 'İzleme listende film yok — bir filme bookmark ekle.'
          }}
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
