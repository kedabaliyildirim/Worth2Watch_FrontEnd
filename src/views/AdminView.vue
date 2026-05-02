<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { Lock, Mail, ShieldCheck } from 'lucide-vue-next'
import AdminComponent from '../components/AdminComponent.vue'

const store = useStore()
const email = ref('')
const password = ref('')
const submitting = ref(false)

const loginState = computed(() => store.getters.getLoginState)

async function login() {
  submitting.value = true
  try {
    await store.dispatch('login', {
      email: email.value,
      password: password.value,
    })
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <main class="max-w-7xl mx-auto px-4 py-12">
    <div
      v-if="!loginState"
      class="max-w-md mx-auto mt-8 bg-slate-900/60 border border-slate-700/60 rounded-2xl p-8 shadow-2xl shadow-black/40"
    >
      <div class="flex items-center gap-3 mb-6">
        <div
          class="w-10 h-10 rounded-lg bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center"
        >
          <ShieldCheck class="text-indigo-300" :size="20" />
        </div>
        <div>
          <h1 class="text-xl font-extrabold text-white">Admin Girişi</h1>
          <p class="text-xs text-slate-500">Sadece yetkili kullanıcılar</p>
        </div>
      </div>

      <form class="space-y-4" @submit.prevent="login">
        <div>
          <label
            class="text-[10px] font-bold uppercase tracking-widest text-slate-500"
            for="admin-email"
          >
            E-posta
          </label>
          <div class="relative mt-1">
            <Mail
              :size="14"
              class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none"
            />
            <input
              id="admin-email"
              v-model="email"
              type="email"
              required
              autocomplete="username"
              class="w-full pl-9 pr-3 py-2.5 bg-slate-950/60 border border-slate-700/60 focus:border-indigo-500/60 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 text-slate-200 placeholder:text-slate-500 rounded-lg text-sm transition-colors"
            />
          </div>
        </div>

        <div>
          <label
            class="text-[10px] font-bold uppercase tracking-widest text-slate-500"
            for="admin-password"
          >
            Şifre
          </label>
          <div class="relative mt-1">
            <Lock
              :size="14"
              class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none"
            />
            <input
              id="admin-password"
              v-model="password"
              type="password"
              required
              autocomplete="current-password"
              class="w-full pl-9 pr-3 py-2.5 bg-slate-950/60 border border-slate-700/60 focus:border-indigo-500/60 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 text-slate-200 placeholder:text-slate-500 rounded-lg text-sm transition-colors"
            />
          </div>
        </div>

        <button
          type="submit"
          :disabled="submitting"
          class="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-60 text-white font-bold rounded-lg transition-colors shadow-lg shadow-indigo-500/20"
        >
          {{ submitting ? 'Bağlanıyor…' : 'Giriş Yap' }}
        </button>

        <p class="text-center text-[11px] text-slate-500">
          Backend bağlı değilse bu form sessizce başarısız olur.
        </p>
      </form>
    </div>

    <AdminComponent v-else />
  </main>
</template>
