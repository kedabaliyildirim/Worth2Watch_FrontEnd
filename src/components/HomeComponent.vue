<template>
  <recomandationComponent v-if="currentPage < 2" />

  <div class="mainBox">
    <div class="sortOptions">
      <label for="sortSelect">Sort by: </label>
      <select id="sortSelect" v-model="sortOption" @change="setSortOption">
        <option value="movieReleaseDate">Release Date</option>
        <option value="imdbRating">IMDB Rating</option>
        <option value="movieName">Movie Name</option>
      </select>
      <label style="margin-left: 30px" for="sortOrderSelect">Sort order:</label>
      <select id="sortOrderSelect" v-model="sortOrder" @change="setSortOption">
        <option value="-1">Ascending</option>
        <option value="1">Descending</option>
      </select>
    </div>
    <div class="row" v-for="(movie, index) in movieStrings" :key="index">
      <router-link :to="{ name: 'movie', params: { id: movie.movie_id } }">
        <!-- poster start -->

        <div class="book">
          <div class="details">
            <p class="movieReleaseDate">{{ movie.movieReleaseDate }}</p>
            <div class="description-3">
              <p class="movieGenre">{{ movie.movieGenre }}</p>
            </div>
            <!-- provider -->
            <div
              style="margin-top: 30px; margin-left: 20px; width: 80%"
              class="providers"
              v-if="movie.movieProviders !== 'No providers available'"
            >
              <div
                v-for="provider in movie.movieProviders"
                :key="provider.provider_id"
                class="provider"
              >
                <img
                  :src="
                    getProviderLogoPath('https://image.tmdb.org/t/p/original' + provider.logo_path)
                  "
                  style="max-width: 22px"
                  alt="Provider Logo"
                  class="providerLogo"
                />
              </div>
            </div>

            <p v-else style="margin-top: 4%">No providers available</p>
          </div>
          <div class="cover">
            <img
              :src="movie.imageURL"
              :alt="movie.movieName + ' Movie Poster'"
              class="poster lazyload"
            />
            <div class="description-2">
              <div class="title-2">
                <p class="title-2">{{ movie.movieName }}</p>
              </div>
              <p class="card-footer-2">{{ movie.movieRuntime }} &nbsp;</p>
            </div>
          </div>
        </div>

        <!-- poster end -->
      </router-link>
    </div>
    <div class="pagination">
      <button class="button" @click="prevPage" :disabled="currentPage === 1">Previous</button>
      <span v-for="pageNumber in visiblePageNumbers" :key="pageNumber">
        <button
          class="button"
          @click="goToPage(pageNumber)"
          :class="{ active: currentPage === pageNumber }"
        >
          {{ pageNumber }}
        </button>
      </span>
      <button class="button" @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    </div>
    <div class="copyright">©w2w</div>
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
            movie_id: parsedMovie._id.$oid,
            movieRuntime: parsedMovie.movieRuntime9dc
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

<style>
.pagination {
  bottom: 0;
  left: 0;
  width: 25%;
  background-color: transparent;
  padding: 1px;
  text-align: center;
}
.button {
  background-color: transparent;
  color: #ccc9dc;
}

.copyright {
  bottom: 0;
  left: 0;
  width: 100%;
  margin-bottom: 10px;
  padding: 1px;
  text-align: center;
  margin-top: 15px;
  font-size: 12px;
}

.description-2 {
  width: 80%;
  margin-top: 10px;
  margin-left: 10px;
  padding: 5px;
  background-color: #00000099;
  backdrop-filter: blur(5px);
  border-radius: 10px;
}
.description-3 {
  margin-left: 20px;
  width: 80%;
  margin-top: 10px;
  padding: 5px;
  background-color: #00000099;
  backdrop-filter: blur(5px);
  border-radius: 10px;
}

.title-2 {
  font-size: 12px;
  max-width: 100%;
  text-align: center;
  color: #008000;
}

.title-2 p {
  width: 100%;
  font-size: 14px;
  font-style: italic;
}

.card-footer-2 {
  color: #ffffff88;
  margin-top: 5px;
  font-size: 10px;
  text-align: right;
}
.book {
  max-height: 440px;
  max-width: 220px;
  flex-direction: column;
  position: relative;
  border-radius: 10px 30px;
  width: 220px;
  height: 300px;
  background-color: #1b2a41;
  -webkit-box-shadow: 1px 1px 12px #fff;
  box-shadow: 0px 0px 8px #ccc9dc;
  -webkit-transform: preserve-3d;
  -ms-transform: preserve-3d;
  transform: preserve-3d;
  -webkit-perspective: 2000px;
  perspective: 2000px;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  -webkit-box-pack: center;
  -ms-flex-pack: center;
  justify-content: center;
  color: #ccc9dc;
}

/* cover */
.cover {
  top: 0;
  position: absolute;
  background-color: #0c1821;
  width: 100%;
  height: 100%;
  border: 1px solid #ccc9dc;
  border-radius: 10px 30px;
  cursor: pointer;
  -webkit-transition: all 0.5s;
  transition: all 0.5s;
  -webkit-transform-origin: 0;
  -ms-transform-origin: 0;
  transform-origin: 0;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  -webkit-box-pack: center;
  -ms-flex-pack: center;
  justify-content: center;
  color: #ccc9dc;
  flex-direction: column;
}

/* cover child elements */
.cover .movieGenre {
  font-weight: bold;
}

.cover .details {
  padding: 15px;
}

.cover .movieName {
  font-style: italic;
  color: #ccc9dc;
  font-size: 15px;
}

.cover .releaseDate {
  align-self: flex-end;
}

.cover .movieGenre {
  font-style: italic;
}

.cover .providers {
  flex-direction: column;
  display: flex;
  padding-left: 20px;
  margin-top: 50px;
  flex-wrap: wrap;
  object-fit: contain;
}

.cover .providerLogo {
  max-width: 20px; /* Adjust max width of provider logo */
}

.book:hover .cover {
  -webkit-transition: all 0.5s;
  transition: all 0.5s;
  -webkit-transform: rotatey(-80deg);
  -ms-transform: rotatey(-80deg);
  transform: rotatey(-80deg);
}

.movie-content-back {
  font-size: 20px;
  font-weight: bolder;
}

/* before */

#headline {
  font-size: 20px;
  color: #ccc9dc;
  margin-top: 2%;
}

.custom-line {
  border: 1px solid black; /* Set the color and style of the line */
  margin: 50px 0px 10px 0px; /* Adjust the margin as needed */
  width: 90%;
  -webkit-box-shadow: 1px 1px 5px #fff;
  box-shadow: 0px 0px 3px #ccc9dc;
}

.mainBox {
  margin-top: 1%;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  width: 90%;
  background-color: transparent; /* Light gray background */
}

.row-2 {
  display: flex;
  justify-content: center;
  margin: 10px 0;
}

.row {
  display: flex;
  justify-content: center;
  margin-top: 70px;
}

.individualBox {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px 0;
  max-height: 440px; /* Adjust max height as needed */
  max-width: 220px; /* Adjust max width as needed */
  color: #ccc9dc;
  margin-right: 4px;
  border: 1px solid #ccc9dc;
  border-radius: 20px;
  background-color: transparent;
}

.individualBox-2 {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px 0;
  max-height: 400px; /* Adjust max height as needed */
  max-width: 100px; /* Adjust max width as needed */
  color: #ccc9dc;
  margin-right: 4px;
  border: 1px solid #ccc9dc;
  border-radius: 20px;
  background-color: transparent;
}

.poster {
  max-width: 60%;
  max-height: 60%; /* Adjust max height of the poster */
  object-fit: cover; /* Ensure the image covers the entire container */
}

.poster-2 {
  max-width: 80%;
  max-height: 80%; /* Adjust max height of the poster */
  object-fit: cover; /* Ensure the image covers the entire container */
}
</style>z