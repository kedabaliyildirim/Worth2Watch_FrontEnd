<script setup>
import { RouterView } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
</script>

<template>
  <div id="app" class="min-h-screen bg-[#0c111a] text-slate-200">
    <AppHeader />
    <RouterView />
  </div>
</template>
