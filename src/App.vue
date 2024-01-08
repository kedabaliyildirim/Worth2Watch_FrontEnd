<!-- emrah -->

<template>
  <div id="app">
    <LoadingIcon v-if="loading" />
    <header>
      <div class="wrapper">
        <div>
          <nav style="margin-left: -200%">
            <span class="logo">W</span><span class="logo-green">2</span
            ><span class="logo" style="margin-right: 70px">W</span>
            <RouterLink class="mainLinks" to="/">HomePage</RouterLink>
            <RouterLink class="mainLinks" to="/admin">Admin</RouterLink>
          </nav>
          <div id="search"><searchComponent /></div>
        </div>
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
import SearchComponent from '@/components/SearchComponent.vue'
import LoadingIcon from '@/components/LoadingIcon.vue' // Import the loading icon component

export default {
  components: {
    SearchComponent,
    LoadingIcon,
    RouterLink,
    RouterView
  },
  data() {
    return {
      searchTerm: '',
      loading: true // Add a variable to control loading icon visibility
    }
  },
  mounted() {
    setTimeout(() => {
      this.loading = false
    }, 2000)
  },

  created() {
    // 1. Dispatch action to get movie data

    this.$store.dispatch('getMovieData', {
      page: 1,
      page_size: 20,
      sort_by: 'movieReleaseDate',
      sort_order: 1
    })
    this.$store.dispatch('getTopTen')

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
.routerview {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-self: center;
  align-content: center;
  align-items: center;
}
.mainLinks {
  margin-left: 15%;
  font-size: 13px;
}
.mainLinks:visited {
  color: #ccc9dc;
}
.mainLinks:active,
.mainLinks:focus {
  color: green;
}
.wrapper {
  display: flex;
  align-content: center;
  background-color: #000000;
  border-radius: 30px;
  justify-content: space-between;
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

.mainLinks.router-link-exact-active {
  color: green;
}
/* Add other styles as needed */
/* Rest of your existing styles... */
</style>
