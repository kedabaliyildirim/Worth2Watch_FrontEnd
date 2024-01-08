<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <LoadingIcon v-if="loading" />
  <MovieComponent :movieObj="currentMovie" />
  
</template>

<script>
import MovieComponent from '../components/MovieComponent.vue'
import LoadingIcon from '../components/LoadingIcon.vue'; // Import the LoadingIcon component

export default {
  components: {
    LoadingIcon,
    MovieComponent,
    
  },
  props: ['movieId'],
  data() {
    return {
      loading: true, // Initialize loading state to true
    };
  },
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
  },

  mounted() {
    // Simulate loading for 3 seconds
    setTimeout(() => {
      this.loading = false; // Set loading to false after 3 seconds
    }, 2000);
  },
}
</script>
