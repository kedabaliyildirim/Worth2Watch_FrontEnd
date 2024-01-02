<template>
  <div class="searchDiv" ref="searchDiv">
    <div class="searchBox">
      <input class="searchInput" type="text" v-model="searchTerm" placeholder="search movie " />
    </div>

    <div v-if="searchResults.length > 0" class="searchResults">
      <div class="searchItem" v-for="movie in searchResults" :key="movie._id" @click="emptyState">
        <RouterLink class="searchLinks" :to="{ name: 'movie', params: { id: movie.movie_id } }">
          <div class="mainSearchContent">
            <img
              :src="movie.imageURL"
              :alt="movie.movieName + ' Movie Poster'"
              class="searchPoster"
            />
            <h4 class="searchTitle">
              {{ movie.movieName }}
            </h4>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script>
import { debounce } from 'lodash'
export default {
  data() {
    return {
      searchTerm: '',
      debouncedSearchInit: debounce(this.searchInit, 1000) // Debounce the searchInit method
    }
  },
  mounted() {
    // Add event listeners when the component is mounted
    document.addEventListener('click', this.handleClickOutside)
    document.addEventListener('keydown', this.handleKeyPress)
  },

  beforeUnmount() {
    // Remove event listeners when the component is about to be destroyed
    document.removeEventListener('click', this.handleClickOutside)
    document.removeEventListener('keydown', this.handleKeyPress)
  },
  methods: {
    searchInit() {
      this.$store.dispatch('searchMovie', this.searchTerm)
    },
    emptyState() {
      this.searchTerm = ''
      this.$store.dispatch('emptySearchResults')
    },
    handleClickOutside(event) {
      // Check if the clicked element is outside the search div
      if (this.$refs.searchDiv && !this.$refs.searchDiv.contains(event.target)) {
        this.emptyState()
      }
    },

    handleKeyPress(event) {
      // Check if the "Esc" key is pressed
      if (event.key === 'Escape') {
        this.emptyState()
      }
    }
  },
  watch: {
    searchTerm() {
      if (this.searchTerm.length >= 2) {
        this.debouncedSearchInit() // Use the debounced function
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
        // Assuming movieGenres is a comma-separated string like "Action, Adventure, Comedy"
        const movieGenres = JSON.parse(movie).movieGenres

        // Split the genres into an array
        const genresArray = movieGenres.split(', ')

        // Get the first two letters of each genre and concatenate them
        const abbreviatedGenres = genresArray.map((genre) => genre.substring(0, 2)).join(' ')
        console.log(abbreviatedGenres) // AC
        console.log(movieGenres[0])
        return {
          movieName: JSON.parse(movie).movieName,
          movieReleaseDate: JSON.parse(movie).movieReleaseDate,
          imageURL: JSON.parse(movie).imageURL,
          movieProviders: provider,
          movieGenre: abbreviatedGenres,
          movie_id: JSON.parse(movie)._id.$oid
        }
      })
    }
  }
}
</script>
