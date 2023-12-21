<template>
  <div id="app">
    <header>
      <div class="wrapper">
        <div class="links">
          <nav>
            <RouterLink class="mainLinks" to="/">Home</RouterLink>
            <RouterLink class="mainLinks" to="/admin">Admin</RouterLink>
          </nav>
        </div>
        <searchComponent />
      </div>
      <div class="routerview">
        <RouterView />
      </div>
    </header>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { RouterLink, RouterView } from 'vue-router'
import searchComponent from '@/components/SearchComponent.vue'

export default {
  components: {
    searchComponent
  },
  data() {
    return {
      searchTerm: ''
    }
  },
  created() {
    // 1. Dispatch action to get movie data
    

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
  },
  methods: {
    searchInit() {
      this.$store.dispatch('searchMovie', this.searchTerm)
    }
  },
  watch: {
    searchTerm() {
      if (this.searchTerm.length >= 2) {
        setTimeout(() => {
          this.searchInit()
        }, 5000)
      }
    }
  },
  computed: {
    searchResults() {
      const movieObject = this.$store.getters.getSearchResults
      let provider = ''
      return movieObject.map((movie) => {
        if (JSON.parse(movie).movieProvider && JSON.parse(movie).movieProvider.US) {
          provider = JSON.parse(movie).movieProvider.US
        } else {
          provider = 'No providers available'
        }
        console.log(JSON.parse(movie))
        return {
          movieName: JSON.parse(movie).movieName,
          movieReleaseDate: JSON.parse(movie).movieReleaseDate,
          movieGenre: JSON.parse(movie).movieGenre,
          imageURL: JSON.parse(movie).imageURL,
          movieProviders: provider,
          movie_id: JSON.parse(movie)._id.$oid
        }
      })
    }
  }
}
</script>

<style>
/* Add other styles as needed */
/* Rest of your existing styles... */
</style>
