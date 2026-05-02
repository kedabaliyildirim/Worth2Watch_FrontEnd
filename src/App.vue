<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useStore } from 'vuex'
import AppHeader from './components/AppHeader.vue'

const store = useStore()

onMounted(() => {
  // Backend yoksa sessizce mock'a düşer (store/actions.js'de fallback var)
  store.dispatch('getTopTen')

  // Token varsa authenticate; yoksa logged-out kal
  let authCookie = null
  const value = `; ${document.cookie}`
  const parts = value.split(`; authToken=`)
  if (parts.length === 2) {
    authCookie = parts.pop().split(';').shift()
  }
  if (authCookie) {
    store.dispatch('setAuthToken', authCookie)
    store.dispatch('authenticate', authCookie)
  }
})
</script>

<template>
  <div id="app" class="min-h-screen bg-[#0c111a] text-slate-200">
    <AppHeader />
    <RouterView />
  </div>
</template>
