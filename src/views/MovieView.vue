<script setup>
import { computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import {
  X,
  Star,
  Clock,
  Calendar,
  ExternalLink,
  Tv,
  Film,
  Layers,
  ThumbsUp,
  ThumbsDown,
  HelpCircle,
  MessageCircle,
} from 'lucide-vue-next'
import LiteYouTubeEmbed from 'vue-lite-youtube-embed'
import 'vue-lite-youtube-embed/style.css'
import Poster from '../components/Poster.vue'
import EpisodeRatingHeatmap from '../components/EpisodeRatingHeatmap.vue'
import { useMovie } from '../composables/useMovies.js'
import { translateGenre } from '../composables/useGenreMap.js'

const props = defineProps({
  id: { type: [String, Number], required: true },
  mediaType: { type: String, default: 'movie' },
})

const router = useRouter()
const movie = useMovie(props.id, props.mediaType)

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

const verdict = computed(() => {
  const m = movie.value
  if (!m) return null
  const v = m.worthVerdict
  if (v === 'worth_watching') {
    return {
      label: 'Worth Watching',
      icon: ThumbsUp,
      panel:
        'bg-gradient-to-br from-emerald-500/15 to-emerald-500/5 border-emerald-500/40',
      pill: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
      score: m.worthScore,
    }
  }
  if (v === 'mixed') {
    return {
      label: 'Mixed Reception',
      icon: HelpCircle,
      panel:
        'bg-gradient-to-br from-yellow-500/15 to-yellow-500/5 border-yellow-500/40',
      pill: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/40',
      score: m.worthScore,
    }
  }
  if (v === 'skip') {
    return {
      label: 'Skip It',
      icon: ThumbsDown,
      panel:
        'bg-gradient-to-br from-red-500/15 to-red-500/5 border-red-500/40',
      pill: 'bg-red-500/20 text-red-300 border-red-500/40',
      score: m.worthScore,
    }
  }
  return null
})

function runtimeFormatted(min, isTv) {
  if (!min) return null
  if (isTv) return `~${min} min/episode`
  const h = Math.floor(min / 60)
  const m = min % 60
  return h > 0 ? `${h}h ${m}m` : `${m}m`
}

function sourceLabel(src) {
  if (!src) return ''
  if (src === 'metrics') return 'Derived from IMDb / TMDB rating statistics'
  if (src.startsWith('groq:')) return 'Synthesised by Llama from real user reviews'
  if (src.startsWith('gemini:')) return 'Synthesised by Gemini from real user reviews'
  return ''
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
      <!-- Close button alone in top-right -->
      <button
        type="button"
        aria-label="Close"
        class="absolute top-3 right-3 z-20 w-9 h-9 flex items-center justify-center rounded-full bg-slate-950/70 hover:bg-slate-800 border border-slate-700/60 text-slate-300 hover:text-white transition-colors"
        @click="close"
      >
        <X :size="18" />
      </button>

      <div class="overflow-y-auto p-6 pr-14 md:pr-16">
        <!-- Header: poster anchored to the BOTTOM-left, content to its right -->
        <div class="flex flex-col md:flex-row gap-6 md:items-end">
          <div
            class="w-40 md:w-44 flex-shrink-0 mx-auto md:mx-0"
          >
            <div
              class="w-full rounded-xl overflow-hidden border border-slate-700/60 shadow-2xl shadow-black/40"
              style="aspect-ratio: 2 / 3"
            >
              <Poster :src="movie.poster" :alt="movie.title" />
            </div>
          </div>

          <div class="flex-1 min-w-0 space-y-5">
            <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
              <!-- LEFT: badge + title + meta -->
              <div class="min-w-0 flex-1">
                <div class="flex items-center gap-2 mb-2">
                  <span
                    class="px-2 py-0.5 rounded text-[9px] font-extrabold uppercase tracking-wider flex items-center gap-1"
                    :class="
                      movie.mediaType === 'tv'
                        ? 'bg-violet-500/20 text-violet-300 border border-violet-500/40'
                        : 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40'
                    "
                  >
                    <component
                      :is="movie.mediaType === 'tv' ? Tv : Film"
                      :size="10"
                    />
                    {{ movie.mediaType === 'tv' ? 'Series' : 'Movie' }}
                  </span>
                  <span
                    v-if="movie.mediaType === 'tv' && movie.seasons"
                    class="text-[10px] font-mono text-slate-400 flex items-center gap-1"
                  >
                    <Layers :size="10" />
                    {{ movie.seasons }}
                    {{ movie.seasons === 1 ? 'season' : 'seasons' }}
                    <template v-if="movie.episodes">
                      · {{ movie.episodes }} episodes
                    </template>
                  </span>
                </div>
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
                  class="flex flex-wrap items-center gap-x-4 gap-y-2 text-sm text-slate-400"
                >
                  <span v-if="movie.releaseDate" class="flex items-center gap-1.5">
                    <Calendar :size="14" />
                    {{ movie.releaseDate }}
                  </span>
                  <!-- Stream provider logos right next to the date,
                       with a clear gap. No label, no border, no chip —
                       just the logos so they read as inline metadata. -->
                  <span
                    v-if="movie.providers && movie.providers.length"
                    class="flex items-center gap-1.5 ml-2"
                    title="Where to watch"
                  >
                    <img
                      v-for="p in movie.providers.slice(0, 4)"
                      :key="p.id"
                      :src="`https://image.tmdb.org/t/p/original${p.logo}`"
                      :alt="p.name"
                      :title="p.name"
                      class="w-6 h-6 rounded-md object-cover ring-1 ring-slate-700/60"
                      loading="lazy"
                    />
                  </span>
                  <span
                    v-if="runtimeFormatted(movie.runtime, movie.mediaType === 'tv')"
                    class="flex items-center gap-1.5"
                  >
                    <Clock :size="14" />
                    {{ runtimeFormatted(movie.runtime, movie.mediaType === 'tv') }}
                  </span>
                  <span v-if="movie.genres && movie.genres.length" class="text-slate-500">·</span>
                  <span class="text-slate-300">
                    {{ (movie.genres || []).map(translateGenre).join(' · ') }}
                  </span>
                </div>
              </div>

              <!-- RIGHT: just the rating chips. The where-to-watch
                   provider pill lives above the poster on the left. -->
              <div class="flex items-center gap-2 flex-wrap lg:justify-end flex-shrink-0">
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
                      <Star :size="13" fill="currentColor" class="inline mr-0.5" />
                      {{ movie.imdbRating.toFixed(1) }}
                    </span>
                    <span
                      v-if="movie.imdbVotes"
                      class="text-[10px] font-mono text-slate-500"
                    >
                      {{ Intl.NumberFormat('en-US').format(movie.imdbVotes) }}
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
                      {{ Intl.NumberFormat('en-US').format(movie.tmdbVotes) }}
                    </span>
                  </div>
              </div>
            </div>

            <!-- Worth verdict — the headline -->
            <div
              v-if="verdict"
              :class="verdict.panel"
              class="rounded-xl border p-4 space-y-3"
            >
              <div class="flex items-center justify-between gap-3">
                <div class="flex items-center gap-2">
                  <img
                    src="/star.png"
                    alt=""
                    class="w-5 h-5 object-contain"
                  />
                  <span class="text-sm font-extrabold uppercase tracking-wide">
                    {{ verdict.label }}
                  </span>
                  <span
                    class="px-2 py-0.5 rounded-md text-[10px] font-bold border"
                    :class="verdict.pill"
                  >
                    {{ verdict.score }}/100
                  </span>
                </div>
                <span
                  v-if="movie.worthSourceCount"
                  class="text-[10px] font-mono text-slate-400 flex items-center gap-1"
                  :title="`Synthesised from ${movie.worthSourceCount} real user reviews`"
                >
                  <MessageCircle :size="10" />
                  {{ movie.worthSourceCount }} reviews
                </span>
              </div>

              <p class="text-sm text-slate-200 leading-relaxed">
                {{ movie.worthSummary }}
              </p>

              <div
                v-if="
                  (movie.worthHighlights && movie.worthHighlights.length) ||
                  (movie.worthLowlights && movie.worthLowlights.length)
                "
                class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2 border-t border-current/15"
              >
                <div
                  v-if="movie.worthHighlights && movie.worthHighlights.length"
                  class="space-y-1.5"
                >
                  <span
                    class="text-[10px] font-bold uppercase tracking-widest text-emerald-400 flex items-center gap-1"
                  >
                    <ThumbsUp :size="10" /> Praised for
                  </span>
                  <ul class="space-y-1">
                    <li
                      v-for="h in movie.worthHighlights"
                      :key="h"
                      class="text-xs text-slate-300 flex items-start gap-1.5"
                    >
                      <span class="text-emerald-400 mt-0.5">+</span>
                      <span>{{ h }}</span>
                    </li>
                  </ul>
                </div>
                <div
                  v-if="movie.worthLowlights && movie.worthLowlights.length"
                  class="space-y-1.5"
                >
                  <span
                    class="text-[10px] font-bold uppercase tracking-widest text-rose-400 flex items-center gap-1"
                  >
                    <ThumbsDown :size="10" /> Criticised for
                  </span>
                  <ul class="space-y-1">
                    <li
                      v-for="l in movie.worthLowlights"
                      :key="l"
                      class="text-xs text-slate-300 flex items-start gap-1.5"
                    >
                      <span class="text-rose-400 mt-0.5">−</span>
                      <span>{{ l }}</span>
                    </li>
                  </ul>
                </div>
              </div>

              <p class="text-[10px] font-mono text-slate-500 pt-1">
                {{ sourceLabel(movie.worthSource) }}
              </p>
            </div>
          </div>
        </div>

        <!-- Wider content below the header (full width) -->
        <div class="mt-6 space-y-6">
          <div
            v-if="
              movie.mediaType === 'tv' &&
              movie.episodeRatings &&
              movie.episodeRatings.length
            "
            class="space-y-2"
          >
            <div class="flex items-center justify-between">
              <span
                class="text-[10px] font-bold uppercase tracking-widest text-slate-500"
              >
                Episode ratings
              </span>
              <span
                v-if="movie.avgEpisodeRating"
                class="text-[10px] font-mono text-slate-400"
              >
                avg
                <span class="font-bold text-emerald-400">
                  {{ movie.avgEpisodeRating.toFixed(1) }}
                </span>
                · {{ movie.episodeRatings.length }} episodes
              </span>
            </div>
            <div
              class="bg-slate-950/40 border border-slate-700/40 rounded-lg p-3 inline-block w-full"
            >
              <EpisodeRatingHeatmap :ratings="movie.episodeRatings" />
            </div>
          </div>

          <div v-if="movie.overview" class="space-y-2">
            <span
              class="text-[10px] font-bold uppercase tracking-widest text-slate-500"
            >
              Synopsis
            </span>
            <p class="text-slate-300 leading-relaxed text-sm">
              {{ movie.overview }}
            </p>
          </div>

          <div v-if="movie.trailerYoutubeId" class="space-y-2 max-w-md mx-auto">
            <div class="flex items-center justify-between">
              <span
                class="text-[10px] font-bold uppercase tracking-widest text-slate-500"
              >
                Trailer
              </span>
              <a
                :href="`https://www.youtube.com/watch?v=${movie.trailerYoutubeId}`"
                target="_blank"
                rel="noopener"
                class="inline-flex items-center gap-1 text-[10px] font-semibold text-slate-500 hover:text-indigo-300 transition-colors"
              >
                YouTube <ExternalLink :size="10" />
              </a>
            </div>
            <div
              class="rounded-lg overflow-hidden border border-slate-700/60 bg-black aspect-video"
            >
              <LiteYouTubeEmbed
                :id="movie.trailerYoutubeId"
                :title="movie.title"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      v-else
      class="relative px-6 py-12 text-center text-slate-400"
      @click.stop
    >
      Movie not found.
    </div>
  </div>
</template>
