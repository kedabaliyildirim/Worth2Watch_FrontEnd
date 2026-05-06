<script setup>
import { computed } from 'vue'
import { Tv, Film } from 'lucide-vue-next'
import Poster from './Poster.vue'

const props = defineProps({
  movie: { type: Object, required: true },
})

const emit = defineEmits(['select'])

const isTv = computed(() => props.movie.mediaType === 'tv')

const scoreColor = computed(() => {
  const s = props.movie.worthScore
  if (s == null) return 'text-slate-500'
  if (s >= 80) return 'text-emerald-400'
  if (s >= 65) return 'text-yellow-400'
  if (s >= 45) return 'text-orange-400'
  return 'text-red-400'
})

</script>

<template>
  <article
    class="group relative cursor-pointer"
    @click="emit('select', movie)"
  >
    <div
      class="relative aspect-[2/3] rounded-xl overflow-hidden bg-slate-900 border border-slate-800/60 group-hover:border-indigo-500/50 shadow-lg group-hover:shadow-indigo-500/20 transition-all duration-200 group-hover:-translate-y-1"
    >
      <Poster :src="movie.poster" :alt="movie.title" />

      <!-- Top-left media-type badge -->
      <span
        class="absolute top-2 left-2 flex items-center gap-1 px-1.5 py-0.5 rounded text-[9px] font-extrabold uppercase tracking-wider backdrop-blur-md"
        :class="
          isTv
            ? 'bg-violet-500/85 text-white'
            : 'bg-cyan-500/85 text-slate-900'
        "
      >
        <component :is="isTv ? Tv : Film" :size="10" />
        {{ isTv ? 'Series' : 'Movie' }}
      </span>

      <!-- Worth score badge — top-right -->
      <div
        v-if="movie.worthScore != null"
        :title="movie.worthSummary"
        class="absolute top-2 right-2 flex items-center gap-1.5 px-2 py-1 rounded-lg bg-slate-950/80 backdrop-blur-md border border-slate-700/40"
      >
        <img src="/star.png" alt="Worth score" class="w-4 h-4 object-contain" />
        <span class="font-black text-base leading-none" :class="scoreColor">
          {{ movie.worthScore }}
        </span>
      </div>

      <!-- Hover overlay with title for accessibility -->
      <div
        class="absolute inset-x-0 bottom-0 h-20 bg-gradient-to-t from-slate-950/95 via-slate-950/60 to-transparent pointer-events-none"
      />
    </div>

    <!-- Title + metadata strip below poster -->
    <div class="mt-2 px-1">
      <h3
        class="text-sm font-bold text-white line-clamp-2 group-hover:text-indigo-300 transition-colors leading-tight"
      >
        {{ movie.title }}
      </h3>
      <div
        class="mt-1 flex items-center gap-2 text-[11px] text-slate-500 font-mono"
      >
        <span v-if="movie.year">{{ movie.year }}</span>
        <template v-if="isTv && movie.seasons">
          <span class="opacity-50">·</span>
          <span class="text-violet-400/80">
            {{ movie.seasons }}
            {{ movie.seasons === 1 ? 'season' : 'seasons' }}
          </span>
        </template>
      </div>
    </div>
  </article>
</template>
