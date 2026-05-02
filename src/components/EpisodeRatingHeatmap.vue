<script setup>
import { computed } from 'vue'

const props = defineProps({
  // Each item: { s: season, e: episode, r: rating, v: votes }
  ratings: { type: Array, required: true },
  compact: { type: Boolean, default: false },
})

const seasons = computed(() => {
  if (!props.ratings || !props.ratings.length) return []
  const bySeason = new Map()
  for (const ep of props.ratings) {
    if (!bySeason.has(ep.s)) bySeason.set(ep.s, [])
    bySeason.get(ep.s).push(ep)
  }
  return [...bySeason.entries()]
    .sort((a, b) => a[0] - b[0])
    .map(([season, eps]) => ({
      season,
      episodes: eps.sort((a, b) => a.e - b.e),
    }))
})

const maxEpisodesPerSeason = computed(() =>
  Math.max(0, ...seasons.value.map((s) => s.episodes.length))
)

// Bant renkleri — kullanıcının tvshow'da onayladığı palet:
// 6.5- kırmızı, 7.x turuncu, 8.x sarı, 9.0+ yeşil. Her bantta üst sınıra
// doğru ton kayar (8.1 ile 8.9 aynı sarı değil).
function colorFor(rating) {
  if (rating == null) return 'rgba(51, 65, 85, 0.5)'
  if (rating >= 9) {
    const t = Math.min(1, (rating - 9) / 1)
    const h = 142 - t * 6 // emerald → green
    const s = 60 + t * 10
    const l = 48 - t * 4
    return `hsl(${h}, ${s}%, ${l}%)`
  }
  if (rating >= 8) {
    const t = (rating - 8) / 1
    const h = 48 - t * 12 // yellow → lime/green direction
    const s = 90 - t * 5
    const l = 55 - t * 8
    return `hsl(${h}, ${s}%, ${l}%)`
  }
  if (rating >= 7) {
    const t = (rating - 7) / 1
    const h = 28 + t * 18 // orange → yellow
    const s = 88
    const l = 55 - t * 4
    return `hsl(${h}, ${s}%, ${l}%)`
  }
  if (rating >= 6) {
    const t = (rating - 6) / 1
    const h = 12 + t * 14 // red-orange → orange
    const s = 78 + t * 10
    const l = 50 + t * 4
    return `hsl(${h}, ${s}%, ${l}%)`
  }
  // < 6
  const t = Math.max(0, rating - 4) / 2
  const h = 0 + t * 10
  const s = 70
  const l = 42 + t * 6
  return `hsl(${h}, ${s}%, ${l}%)`
}
</script>

<template>
  <div
    v-if="seasons.length"
    class="space-y-1"
    :class="compact ? 'text-[8px]' : 'text-[10px]'"
  >
    <div
      v-for="row in seasons"
      :key="row.season"
      class="flex items-center gap-1.5"
    >
      <span
        class="font-mono text-slate-500 flex-shrink-0"
        :class="compact ? 'w-5' : 'w-7'"
      >
        S{{ row.season }}
      </span>
      <div class="flex items-center gap-[2px] flex-wrap">
        <span
          v-for="ep in row.episodes"
          :key="`${row.season}-${ep.e}`"
          :title="`S${row.season}E${ep.e} · ${ep.r.toFixed(1)} (${Intl.NumberFormat('tr-TR').format(ep.v)} oy)`"
          class="rounded-[2px] flex items-center justify-center text-slate-900 font-bold cursor-default"
          :class="compact ? 'w-3 h-3 text-[6px]' : 'w-5 h-5 text-[9px]'"
          :style="{ backgroundColor: colorFor(ep.r) }"
        >
          <template v-if="!compact && ep.r >= 8">{{ Math.round(ep.r * 10) / 10 }}</template>
        </span>
      </div>
    </div>
  </div>
  <div
    v-else
    class="text-xs text-slate-500 italic"
  >
    Bölüm puanı verisi yok.
  </div>
</template>
