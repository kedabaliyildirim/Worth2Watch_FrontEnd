<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { Film, Search } from 'lucide-vue-next'
import { useGlobalSearch } from '../composables/useGlobalSearch.js'

const search = useGlobalSearch()
const value = computed({
  get: () => search.term.value,
  set: (v) => search.setTerm(v),
})
</script>

<template>
  <header
    class="sticky top-0 z-30 backdrop-blur-xl bg-slate-950/55 border-b border-slate-800/60"
  >
    <div
      class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between gap-4"
    >
      <RouterLink
        to="/"
        class="flex items-center gap-2 group focus:outline-none flex-shrink-0"
      >
        <div
          class="w-9 h-9 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/30 group-hover:scale-105 transition-transform"
        >
          <Film :size="18" class="text-white" />
        </div>
        <div class="text-base font-extrabold text-white tracking-tight leading-none">
          Worth<span class="text-indigo-400">2</span>Watch
        </div>
      </RouterLink>

      <div class="relative flex-1 max-w-xl">
        <Search
          :size="16"
          class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none"
        />
        <input
          v-model="value"
          type="search"
          placeholder="Search movies and series..."
          aria-label="Search movies and series"
          class="w-full pl-9 pr-3 py-2 bg-slate-800/40 border border-slate-700/50 focus:border-indigo-500/60 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 text-slate-200 placeholder:text-slate-500 rounded-lg text-sm transition-colors"
        />
      </div>
    </div>
  </header>
</template>
