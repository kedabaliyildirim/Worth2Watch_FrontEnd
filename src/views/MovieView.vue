<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <MovieComponent :movieObj="currentMovie" />
</template>

<script>
import MovieComponent from '../components/MovieComponent.vue'
export default {
  components: {
    MovieComponent
  },
  props: ['movieId'],
  computed: {
    currentMovie() {
      const movieObj = this.$store.getters.getCurrentMovie
      const movieProvider = JSON.parse(movieObj).movieProvider.US
      let comments = []
      if (JSON.parse(movieObj).Comments) {
        comments = JSON.parse(movieObj).Comments
      } else {
        comments = {
          youtubeComments: [],
          redditComments: []
        }
      }
      return {
        movieName: JSON.parse(movieObj).movieName,
        movieReleaseDate: JSON.parse(movieObj).movieReleaseDate,
        movieGenre: JSON.parse(movieObj).movieGenres,
        imageURL: JSON.parse(movieObj).imageURL,
        movieDuration: JSON.parse(movieObj).movieRuntime,
        movieDirector: JSON.parse(movieObj).movieDirector,
        movieWriter: JSON.parse(movieObj).movieWriter,
        movieScore: JSON.parse(movieObj).movieScore,
        movieActors: JSON.parse(movieObj).movieActors,
        description: JSON.parse(movieObj).movieDescription,
        movieComments: comments,
        movieProviders: movieProvider
      }
    }
    // For demo purposes, using Lorem Ipsum for comments
  }
}
</script>
