<template>
  <div class="divBody">
    <header>
      <div class="wrapper">
        <nav>
          <RouterLink class="RouteLink" to="/">Home</RouterLink>
          <RouterLink class="RouteLink" to="/admin">Admin</RouterLink>
        </nav>
      </div>
      <RouterView class="routerview" />
    </header>
  </div>
</template>
<script>
// eslint-disable-next-line no-unused-vars
import { RouterLink, RouterView } from 'vue-router'
// eslint-disable-next-line no-unused-vars
export default {
  created() {
    // 1. Dispatch action to get movie data
    this.$store.dispatch('getMovieData')
    // 2. Check for authentication token in the Vuex store
    const authToken = this.$store.getters.getAuthToken
    if (authToken) {
      // 2a. If present, dispatch action to authenticate
      this.$store.dispatch('authenticate', authToken)
    } else {
      // 3. Check for authentication token in cookies
      let authCookie = null
      const value = `; ${document.cookie}`
      const parts = value.split(`; ${'authToken'}=`)
      if (parts.length === 2) {
        authCookie = parts.pop().split(';').shift()
      } else {
        authCookie = null
      }
      if (authCookie) {
        // 4. If found, extract token, set in store, and dispatch action to authenticate
        const token = authCookie.split('=')[1]
        this.$store.dispatch('setAuthToken', token)
        this.$store.dispatch('authenticate', authCookie)
      } else {
        console.log('no auth token found')
      }
    }
  }
}
</script>

<style>
.divBody {
  display: flex;
  flex-direction: column;
  place-items: center;
  align-content: center;
  justify-content: center;
  flex-wrap: wrap;

  padding: 1rem; /* Add padding to the wrapper for better spacing */
}
.wrapper {
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  align-content: flex-start;
  padding: 1rem; /* Add padding to the wrapper for better spacing */
}

.RouteLink {
  margin: 15%;
}

header {
  display: flex;
  flex-direction: column;
  align-content: center;
  justify-content: center;
  align-items: center;
}
nav a.router-link-exact-active {
  color: var(--color-text);
}
/* Add other styles as needed */

/* Rest of your existing styles... */
</style>
<!-- <template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

</style> -->
