<!-- EMRAH -->
<template>
   <h2 id="headline">Top 10 Movies</h2>
  <div class="mainBox">
    <div class="row-2" v-for="(movie, index) in movieStrings" :key="index">
      <router-link :to="{ name: 'movie', params: { id: movie.movie_id } }">
        <div class="individualBox-2">
          <img
            :src="movie.imageURL"
            :alt="movie.movieName + ' Movie Poster'"
            class="poster-2 lazyload"
          />
          <div class="details">
            <h3 class="movieName">{{ movie.movieName }}</h3>
          </div>
        </div>
      </router-link>
    </div>
  </div>
  <hr class="custom-line">
</template>

<script>
export default {
  computed: {
    movieStrings() {
      const movieObject = this.$store.getters.getTopTenMovies
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
    }
  }
}
</script>
