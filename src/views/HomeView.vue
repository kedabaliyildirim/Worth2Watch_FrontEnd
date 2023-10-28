<template>
  <RouterLink to="/admin"></RouterLink>
 <HomeComponent :movieStrings="movieStrings" />
</template>
<script>
import HomeComponent from '../components/HomeComponent.vue'
export default {
  components: {
    HomeComponent
  },
  computed: {
    movieStrings() {
      const movieObject = this.$store.getters.getMovies
      let provider = ''
      return movieObject.map((movie) => {
        if (JSON.parse(movie).movieProvider && JSON.parse(movie).movieProvider.US) {
          provider = JSON.parse(movie).movieProvider.US
        } else {
          provider = 'No providers available'
        }
        return {
          movieName: JSON.parse(movie).movieName,
          movieReleaseDate: JSON.parse(movie).movieReleaseDate,
          movieGenre: JSON.parse(movie).movieGenre,
          imageURL: JSON.parse(movie).imageURL,
          movieProviders: provider
        }
      })
    }
  }

}
</script>
