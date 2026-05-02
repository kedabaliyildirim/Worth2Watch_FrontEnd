<script setup>
import { computed } from 'vue'
import {
  Star,
  Clock,
  Bookmark,
  Tv,
  Film,
  ThumbsUp,
  ThumbsDown,
  HelpCircle,
} from 'lucide-vue-next'
import Poster from './Poster.vue'
import EpisodeRatingHeatmap from './EpisodeRatingHeatmap.vue'

const props = defineProps({
  movie: { type: Object, required: true },
  index: { type: Number, default: 0 },
  inWatchlist: { type: Boolean, default: false },
})

const emit = defineEmits(['select', 'toggleWatchlist'])

const isTv = computed(() => props.movie.mediaType === 'tv')

const runtime = computed(() => {
  const r = props.movie.runtime
  if (!r) return null
  if (isTv.value) return `~${r}d/böl`
  const h = Math.floor(r / 60)
  const m = r % 60
  return h > 0 ? `${h}s ${m}d` : `${m}d`
})

const seasonsLine = computed(() => {
  if (!isTv.value) return null
  const s = props.movie.seasons
  const e = props.movie.episodes
  if (!s) return null
  const seasonStr = `${s} sezon`
  return e ? `${seasonStr} · ${e} bölüm` : seasonStr
})

const genreLine = computed(() => {
  const g = props.movie.genres
  if (!g || !g.length) return ''
  return g.slice(0, 3).join(' · ')
})

function ratingColor(score) {
  if (!score && score !== 0) return 'text-slate-400'
  if (score >= 8) return 'text-emerald-400'
  if (score >= 7) return 'text-yellow-400'
  if (score >= 6) return 'text-orange-400'
  return 'text-red-400'
}

const verdict = computed(() => {
  const v = props.movie.worthVerdict
  const score = props.movie.worthScore
  if (v === 'izlemeye_değer') {
    return {
      label: 'İzle',
      icon: ThumbsUp,
      classes: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
      score,
    }
  }
  if (v === 'tartışmalı') {
    return {
      label: 'Bölüyor',
      icon: HelpCircle,
      classes: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/40',
      score,
    }
  }
  if (v === 'izleme') {
    return {
      label: 'Pas geç',
      icon: ThumbsDown,
      classes: 'bg-red-500/20 text-red-300 border-red-500/40',
      score,
    }
  }
  return null
})

function onBookmarkClick(e) {
  e.stopPropagation()
  emit('toggleWatchlist', `${props.movie.mediaType}-${props.movie.tmdbId}`)
}
</script>

<template>
  <div
    class="group relative flex items-center gap-4 p-4 bg-slate-800/40 hover:bg-slate-800 border border-slate-700/50 hover:border-indigo-500/50 rounded-xl transition-[colors,transform,box-shadow] duration-200 cursor-pointer mb-3 hover:-translate-y-0.5 hover:shadow-[0_8px_24px_-12px_rgba(168,85,247,0.4)]"
    @click="emit('select', movie)"
  >
    <button
      type="button"
      :aria-label="
        inWatchlist ? 'İzleme listesinden çıkar' : 'İzleme listesine ekle'
      "
      :aria-pressed="inWatchlist"
      class="absolute top-2 right-2 z-10 p-1.5 rounded-lg transition-colors"
      :class="
        inWatchlist
          ? 'text-indigo-400 hover:text-indigo-300'
          : 'text-slate-600 hover:text-indigo-300 opacity-0 group-hover:opacity-100 focus:opacity-100'
      "
      @click="onBookmarkClick"
    >
      <Bookmark :size="18" :fill="inWatchlist ? 'currentColor' : 'none'" />
    </button>

    <div
      class="w-8 text-center font-mono text-slate-500 text-sm font-bold flex-shrink-0"
    >
      #{{ index }}
    </div>

    <div
      class="relative w-16 h-24 flex-shrink-0 rounded-lg overflow-hidden shadow-lg border border-slate-700/50 group-hover:scale-105 transition-transform duration-300"
      style="will-change: transform"
    >
      <Poster :src="movie.poster" :alt="movie.title" />
      <span
        class="absolute top-1 left-1 px-1 py-0.5 rounded text-[8px] font-extrabold uppercase tracking-wider backdrop-blur-md"
        :class="
          isTv
            ? 'bg-violet-500/85 text-white'
            : 'bg-cyan-500/85 text-slate-900'
        "
      >
        {{ isTv ? 'Dizi' : 'Film' }}
      </span>
    </div>

    <div class="flex-1 min-w-0">
      <div class="flex items-center gap-2 mb-1">
        <component
          :is="isTv ? Tv : Film"
          :size="14"
          :class="isTv ? 'text-violet-400' : 'text-cyan-400'"
          class="flex-shrink-0"
        />
        <h3
          class="text-lg font-bold text-white truncate group-hover:text-indigo-300 transition-colors duration-300"
        >
          {{ movie.title }}
        </h3>
        <span v-if="movie.year" class="text-xs text-slate-500 font-mono">
          {{ movie.year }}
        </span>
      </div>
      <div
        class="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-slate-400"
      >
        <span
          class="flex items-center gap-1 font-semibold"
          :class="ratingColor(movie.imdbRating)"
        >
          <Star :size="14" fill="currentColor" />
          {{ movie.imdbRating ? movie.imdbRating.toFixed(1) : '—' }}
        </span>
        <span class="w-1 h-1 bg-slate-600 rounded-full" />
        <span class="truncate max-w-[280px]">
          {{ genreLine }}
        </span>
        <template v-if="runtime">
          <span class="w-1 h-1 bg-slate-600 rounded-full" />
          <span class="flex items-center gap-1 text-slate-400">
            <Clock :size="12" />
            {{ runtime }}
          </span>
        </template>
        <template v-if="seasonsLine">
          <span class="w-1 h-1 bg-slate-600 rounded-full" />
          <span class="text-violet-400 font-semibold text-xs">
            {{ seasonsLine }}
          </span>
        </template>
        <template v-if="verdict">
          <span class="w-1 h-1 bg-slate-600 rounded-full" />
          <span
            :title="movie.worthSummary"
            class="flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-bold border"
            :class="verdict.classes"
          >
            <component :is="verdict.icon" :size="10" />
            {{ verdict.label }}
            <span
              v-if="verdict.score != null"
              class="font-mono opacity-80"
            >
              · {{ verdict.score }}
            </span>
          </span>
        </template>
      </div>
    </div>

    <div class="hidden lg:flex items-center gap-8 mr-4">
      <!-- Worth score: the brand verdict, prominent and always present -->
      <div class="flex flex-col items-center w-14" v-if="verdict">
        <span
          class="text-[8px] font-extrabold uppercase tracking-wider text-slate-500"
        >
          Worth
        </span>
        <span
          class="text-2xl font-black leading-none mt-0.5"
          :class="
            verdict.label === 'İzle'
              ? 'text-emerald-400'
              : verdict.label === 'Pas geç'
                ? 'text-red-400'
                : 'text-yellow-400'
          "
        >
          {{ movie.worthScore != null ? movie.worthScore : '—' }}
        </span>
      </div>
      <div class="flex flex-col items-center w-14" v-else>
        <span
          class="text-[8px] font-extrabold uppercase tracking-wider text-slate-700"
        >
          Worth
        </span>
        <span class="text-2xl font-black leading-none mt-0.5 text-slate-700">
          —
        </span>
      </div>

      <div class="flex flex-col items-center w-14">
        <span
          class="w-7 h-7 rounded-sm flex items-center justify-center text-[8px] font-extrabold text-slate-900"
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
          class="text-sm font-bold mt-1"
          :class="ratingColor(movie.tmdbRating)"
        >
          {{ movie.tmdbRating ? movie.tmdbRating.toFixed(1) : '—' }}
        </span>
      </div>

      <!-- TV: episode heatmap; movies: provider strip in same column -->
      <div
        v-if="isTv && movie.episodeRatings && movie.episodeRatings.length"
        class="w-44 max-h-20 overflow-hidden"
      >
        <EpisodeRatingHeatmap :ratings="movie.episodeRatings.slice(0, 60)" compact />
      </div>
      <div
        v-else-if="movie.providers && movie.providers.length"
        class="flex items-center gap-1.5 w-32"
      >
        <img
          v-for="p in movie.providers.slice(0, 4)"
          :key="p.id"
          :src="`https://image.tmdb.org/t/p/original${p.logo}`"
          :alt="p.name"
          :title="p.name"
          class="w-7 h-7 rounded object-cover ring-1 ring-slate-700/60"
          loading="lazy"
        />
      </div>
      <div v-else class="w-32 text-xs text-slate-500 italic">Türkiye'de yok</div>
    </div>
  </div>
</template>
