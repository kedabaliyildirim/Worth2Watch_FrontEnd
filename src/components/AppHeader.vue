<script setup>
import { RouterLink } from 'vue-router'
import { Film } from 'lucide-vue-next'
</script>

<template>
  <header
    class="sticky top-0 z-30 backdrop-blur-xl bg-slate-950/70 border-b border-slate-800/60"
  >
    <div
      class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between gap-4"
    >
      <RouterLink
        to="/"
        class="flex items-center gap-2 group focus:outline-none"
      >
        <div
          class="w-9 h-9 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/30 group-hover:scale-105 transition-transform"
        >
          <Film :size="18" class="text-white" />
        </div>
        <div class="leading-none">
          <div class="text-base font-extrabold text-white tracking-tight">
            Worth<span class="text-indigo-400">2</span>Watch
          </div>
          <div class="text-[10px] font-mono text-slate-500 tracking-widest">
            FILMS · CURATED
          </div>
        </div>
      </RouterLink>

      <nav class="flex items-center gap-1">
        <RouterLink
          to="/"
          class="px-3 py-1.5 text-sm font-semibold rounded-lg transition-colors text-slate-400 hover:text-white hover:bg-slate-800/60"
          active-class="text-white bg-slate-800"
        >
          Keşfet
        </RouterLink>
      </nav>
    </div>
  </header>
</template>
