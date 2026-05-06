<script setup>
import { ref } from 'vue'

const props = defineProps({
  src: { type: String, default: '' },
  alt: { type: String, default: '' },
})

const errored = ref(false)
const loaded = ref(false)
</script>

<template>
  <div class="relative w-full h-full bg-slate-950 overflow-hidden">
    <div
      v-if="!loaded && !errored"
      class="absolute inset-0 bg-gradient-to-br from-slate-800 to-slate-900 animate-pulse"
    />
    <img
      v-if="src && !errored"
      :src="src"
      :alt="alt"
      loading="lazy"
      decoding="async"
      class="w-full h-full object-cover transition-opacity duration-500"
      :class="loaded ? 'opacity-100' : 'opacity-0'"
      @load="loaded = true"
      @error="errored = true"
    />
    <div
      v-if="!src || errored"
      class="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-slate-800 to-slate-950 text-slate-500 text-xs font-bold tracking-wide text-center px-2"
    >
      {{ alt || 'POSTER YOK' }}
    </div>
  </div>
</template>
