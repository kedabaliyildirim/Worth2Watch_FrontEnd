<template>
  <recomandationComponent />
  <div class="mainBox">
    <div class="sortOptions">
      <h1>{{ sortOrder }}</h1>
      <label for="sortSelect">Sort by:</label>
      <select id="sortSelect" v-model="sortOption" @change="setSortOption">
        <option value="movieName">Movie Name</option>
        <option value="movieReleaseDate">Release Date</option>
        <option value="imdbRating">IMDB Rating</option>
        <option value="tmdbRating">TMDB Rating</option>
      </select>
      <label for="sortOrderSelect">Sort order:</label>
      <select id="sortOrderSelect" v-model="sortOrder" @change="setSortOption">
        <option value="1">Descending</option>
        <option value="-1">Ascending</option>
      </select>
    </div>
    <div class="row" v-for="(movie, index) in movieStrings" :key="index">
      <router-link :to="{ name: 'movie', params: { id: movie.movie_id } }">
        <div class="individualBox">
          <p class="releaseDate">{{ movie.movieReleaseDate }}</p>
          <img
            :src="movie.imageURL"
            :alt="movie.movieName + ' Movie Poster'"
            class="poster lazyload"
          />
          <div class="details">
            <h3 class="movieName">{{ movie.movieName }}</h3>
            <p class="movieGenre">{{ movie.movieGenre }}</p>
            <div class="providers" v-if="movie.movieProviders !== 'No providers available'">
              <div
                v-for="provider in movie.movieProviders"
                :key="provider.provider_id"
                class="provider"
              >
                <img
                  :src="
                    getProviderLogoPath('https://image.tmdb.org/t/p/original' + provider.logo_path)
                  "
                  alt="Provider Logo"
                  class="providerLogo"
                />
                {{ provider.provider_name }}
              </div>
            </div>
            <p v-else style="margin-top: 4%">No providers available</p>
          </div>
        </div>
      </router-link>
    </div>
  </div>

  <div class="pagination">
    <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
    <span v-for="pageNumber in visiblePageNumbers" :key="pageNumber">
      <button @click="goToPage(pageNumber)" :class="{ active: currentPage === pageNumber }">
        {{ pageNumber }}
      </button>
    </span>
    <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
  </div>
</template>

<script>
import recomandationComponent from './RecomandationComponent.vue'
export default {
  components: {
    // eslint-disable-next-line vue/no-unused-components
    recomandationComponent
  },
  data() {
    return {
      itemsPerPage: 20,
      currentPage: 1,
      sortOption: 'movieName',
      sortOrder: 1
    }
  },
  computed: {
    totalPages() {
      return this.$store.getters.getTotalPageCount
    },
    movieStrings() {
      const movieObject = this.$store.getters.getMovies
      let provider = ''
      return movieObject.map((movie) => {
        try {
          const parsedMovie = JSON.parse(movie)
          if (parsedMovie.movieProvider && parsedMovie.movieProvider.US) {
            provider = parsedMovie.movieProvider.US
          } else {
            provider = 'No providers available'
          }
          return {
            movieName: parsedMovie.movieName,
            movieReleaseDate: parsedMovie.movieReleaseDate,
            movieGenre: parsedMovie.movieGenres,
            imageURL: parsedMovie.imageURL,
            movieProviders: provider,
            movie_id: parsedMovie._id.$oid
          }
        } catch (error) {
          console.log(error)
        }
      })
    },

    visiblePageNumbers() {
      const totalVisiblePages = 6 // 3 before current, current, 2 after current
      const halfVisiblePages = Math.floor(totalVisiblePages / 2)
      let startPage = Math.max(1, this.currentPage - halfVisiblePages)
      let endPage = Math.min(this.totalPages, startPage + totalVisiblePages - 1)

      if (endPage - startPage + 1 < totalVisiblePages) {
        startPage = Math.max(1, endPage - totalVisiblePages + 1)
      }

      return Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i)
    }
  },
  methods: {
    getProviderLogoPath(logoPath) {
      return `https://image.tmdb.org/t/p/original${logoPath}`
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
        this.$store.dispatch('getMovieData', { page: this.currentPage, page_size: 20 })
      }
    },
    goToPage(pageNumber) {
      this.currentPage = pageNumber
    },
    setSortOption() {
      const payload = {
        page: this.currentPage,
        page_size: this.itemsPerPage,
        sort_by: this.sortOption,
        sort_order: parseInt(this.sortOrder) // Convert sortOrder to a number
      }
      this.$store.dispatch('getMovieData', payload)
    }
  }
}
</script>
