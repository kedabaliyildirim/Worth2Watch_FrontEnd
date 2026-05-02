<script setup>
import { onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import {
  X,
  Star,
  Clock,
  Calendar,
  Bookmark,
  ExternalLink,
} from 'lucide-vue-next'
import LiteYouTubeEmbed from 'vue-lite-youtube-embed'
import 'vue-lite-youtube-embed/style.css'
import Poster from '../components/Poster.vue'
import { useMovie } from '../composables/useMovies.js'
import { useWatchlist } from '../composables/useWatchlist.js'

const props = defineProps({ id: { type: [String, Number], required: true } })

const router = useRouter()
const movie = useMovie(props.id)
const watchlist = useWatchlist()

function close() {
  if (window.history.length > 1) router.back()
  else router.push('/')
}

function onKey(e) {
  if (e.key === 'Escape') close()
}

onMounted(() => {
  document.body.style.overflow = 'hidden'
  document.addEventListener('keydown', onKey)
})

onBeforeUnmount(() => {
  document.body.style.overflow = ''
  document.removeEventListener('keydown', onKey)
})

function ratingColor(score) {
  if (!score && score !== 0) return 'text-slate-400'
  if (score >= 8) return 'text-emerald-400'
  if (score >= 7) return 'text-yellow-400'
  if (score >= 6) return 'text-orange-400'
  return 'text-red-400'
}

function runtimeFormatted(min) {
  if (!min) return null
  const h = Math.floor(min / 60)
  const m = min % 60
  return h > 0 ? `${h}s ${m}d` : `${m}d`
}
</script>

<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-8"
    @click.self="close"
  >
    <div
      class="absolute inset-0 bg-slate-950/55 backdrop-blur-xl pointer-events-none"
      :style="
        movie?.backdrop
          ? `background-image: url('${movie.backdrop}'); background-size: cover; background-position: center;`
          : ''
      "
    />
    <div
      class="absolute inset-0 bg-gradient-to-b from-slate-950/70 via-slate-950/85 to-slate-950 pointer-events-none"
    />

    <div
      v-if="movie"
      class="relative w-full max-w-5xl max-h-[90vh] bg-slate-900/95 border border-slate-700/60 rounded-2xl shadow-2xl shadow-black/60 overflow-hidden flex flex-col animate-fade-in"
      @click.stop
    >
      <button
        type="button"
        aria-label="Kapat"
        class="absolute top-4 right-4 z-20 w-9 h-9 flex items-center justify-center rounded-full bg-slate-950/70 hover:bg-slate-800 border border-slate-700/60 text-slate-300 hover:text-white transition-colors"
        @click="close"
      >
        <X :size="18" />
      </button>

      <div
        class="grid grid-cols-1 md:grid-cols-[220px_1fr] gap-6 p-6 overflow-y-auto"
      >
        <div class="flex justify-center md:justify-start">
          <div
            class="w-44 md:w-52 aspect-[2/3] rounded-xl overflow-hidden border border-slate-700/60 shadow-2xl shadow-black/40 flex-shrink-0"
          >
            <Poster :src="movie.poster" :alt="movie.title" />
          </div>
        </div>

        <div class="min-w-0 space-y-5">
          <div>
            <h1 class="text-3xl font-extrabold text-white tracking-tight mb-2">
              {{ movie.title }}
            </h1>
            <div
              v-if="movie.originalTitle && movie.originalTitle !== movie.title"
              class="text-sm text-slate-500 italic mb-2"
            >
              {{ movie.originalTitle }}
            </div>
            <div
              class="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-slate-400"
            >
              <span v-if="movie.releaseDate" class="flex items-center gap-1.5">
                <Calendar :size="14" />
                {{ movie.releaseDate }}
              </span>
              <span
                v-if="runtimeFormatted(movie.runtime)"
                class="flex items-center gap-1.5"
              >
                <Clock :size="14" />
                {{ runtimeFormatted(movie.runtime) }}
              </span>
              <span v-if="movie.genres && movie.genres.length" class="text-slate-500">·</span>
              <span class="text-slate-300">{{ (movie.genres || []).join(' · ') }}</span>
            </div>
          </div>

          <div class="flex flex-wrap items-center gap-3">
            <div
              v-if="movie.imdbRating != null"
              class="flex items-center gap-2 px-3 py-2 bg-slate-800/60 border border-slate-700/50 rounded-lg"
            >
              <span
                class="w-7 h-5 rounded bg-yellow-500 text-slate-900 text-[9px] font-extrabold flex items-center justify-center"
              >
                IMDb
              </span>
              <span
                class="font-bold text-base"
                :class="ratingColor(movie.imdbRating)"
              >
                <Star :size="14" fill="currentColor" class="inline mr-1" />
                {{ movie.imdbRating.toFixed(1) }}
              </span>
              <span
                v-if="movie.imdbVotes"
                class="text-[10px] font-mono text-slate-500"
              >
                {{ Intl.NumberFormat('tr-TR').format(movie.imdbVotes) }}
              </span>
            </div>

            <div
              v-if="movie.tmdbRating != null"
              class="flex items-center gap-2 px-3 py-2 bg-slate-800/60 border border-slate-700/50 rounded-lg"
            >
              <span
                class="w-6 h-6 rounded text-[8px] font-extrabold flex items-center justify-center text-slate-900"
                style="
                  background: linear-gradient(
                    135deg,
                    #0d253f 0%,
                    #01b4e4 50%,
                    #90cea1 100%
                  );
                "
              >
                T
              </span>
              <span
                class="font-bold text-base"
                :class="ratingColor(movie.tmdbRating)"
              >
                {{ movie.tmdbRating.toFixed(1) }}
              </span>
              <span
                v-if="movie.tmdbVotes"
                class="text-[10px] font-mono text-slate-500"
              >
                {{ Intl.NumberFormat('tr-TR').format(movie.tmdbVotes) }}
              </span>
            </div>

            <button
              type="button"
              :aria-pressed="watchlist.has(movie.tmdbId)"
              class="ml-auto flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-bold border transition-all"
              :class="
                watchlist.has(movie.tmdbId)
                  ? 'bg-indigo-500 text-white border-indigo-400 shadow-[0_0_18px_rgba(99,102,241,0.35)]'
                  : 'bg-slate-800/60 text-slate-300 border-slate-700/60 hover:border-indigo-500/50 hover:text-white'
              "
              @click="watchlist.toggle(movie.tmdbId)"
            >
              <Bookmark
                :size="14"
                :fill="watchlist.has(movie.tmdbId) ? 'currentColor' : 'none'"
              />
              {{ watchlist.has(movie.tmdbId) ? 'Listemde' : 'Listeme ekle' }}
            </button>
          </div>

          <div
            v-if="movie.providers && movie.providers.length"
            class="flex items-center gap-3 flex-wrap"
          >
            <span
              class="text-[10px] font-bold uppercase tracking-widest text-slate-500"
            >
              Türkiye'de nerede izlenir
            </span>
            <div class="flex items-center gap-2">
              <img
                v-for="p in movie.providers"
                :key="p.id"
                :src="`https://image.tmdb.org/t/p/original${p.logo}`"
                :alt="p.name"
                :title="p.name"
                class="w-9 h-9 rounded-lg object-cover ring-1 ring-slate-700/60"
                loading="lazy"
              />
            </div>
          </div>

          <div v-if="movie.overview" class="space-y-2">
            <span
              class="text-[10px] font-bold uppercase tracking-widest text-slate-500"
            >
              Özet
            </span>
            <p class="text-slate-300 leading-relaxed text-sm">
              {{ movie.overview }}
            </p>
          </div>

          <div v-if="movie.trailerYoutubeId" class="space-y-2">
            <span
              class="text-[10px] font-bold uppercase tracking-widest text-slate-500"
            >
              Fragman
            </span>
            <div
              class="rounded-xl overflow-hidden border border-slate-700/60 bg-black"
            >
              <LiteYouTubeEmbed
                :id="movie.trailerYoutubeId"
                :title="movie.title"
              />
            </div>
            <a
              :href="`https://www.youtube.com/watch?v=${movie.trailerYoutubeId}`"
              target="_blank"
              rel="noopener"
              class="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-indigo-300 transition-colors"
            >
              YouTube'da aç <ExternalLink :size="12" />
            </a>
          </div>
        </div>
      </div>
    </div>

    <div
      v-else
      class="relative px-6 py-12 text-center text-slate-400"
      @click.stop
    >
      Film bulunamadı.
    </div>
  </div>
</template>
