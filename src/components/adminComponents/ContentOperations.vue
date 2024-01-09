<template>
  <div class="adminContentHeader">
    <button @click="logout" class="logoutButton">Logout</button>
    <p>Admin Operations</p>
  </div>

  <div class="adminContentBody">
    <form class="pullCommentsForm" @submit.prevent>
      <h3>Pull Comments</h3>
      <label>Select platforms:</label>
      <div>
        <label>
          <input type="checkbox" v-model="platformsToPull.youtube" />
          YouTube
        </label>
        <label>
          <input type="checkbox" v-model="platformsToPull.reddit" />
          Reddit
        </label>
        <!-- Add more platforms as needed -->
      </div>
      <button @click="pullComments" type="submit">Pull Comments</button>
    </form>
    <form class="pullCommentsForm" @submit.prevent>
      <h3>Sentiment Analysis</h3>
      <label>Select platforms:</label>
      <div>
        <label>
          <input type="checkbox" v-model="platformsToAnalyse.youtube" />
          YouTube
        </label>
        <label>
          <input type="checkbox" v-model="platformsToAnalyse.reddit" />
          Reddit
        </label>
        <!-- Add more platforms as needed -->
      </div>
      <button @click="analyseSentiment" type="submit">Sentiment Analysis</button>
    </form>
    <!-- Pull Movies Form -->
    <form class="pullMoviesForm" @submit.prevent>
      <h3>Pull Movies</h3>
      <button @click="pullMovies">Pull Movies</button>
    </form>
    <!-- Admin Deletion Form -->
    <div class="dangerZone">
      <h3>Danger Zone</h3>
      <form @submit.prevent>
        <button @click="removeAllComments" type="submit">Remove All Comments</button>
      </form>
      <form @submit.prevent>
        <button @click="removeDb('content')">Remove All Movies</button>
      </form>
      <form @submit.prevent>
        <button @click="removeDb('popular_movies')">Remove All Popular_movies</button>
        <button @click="testPopDb" class="logoutButton">pull Popular_movies</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // ... (previous data)
      platformsToPull: {
        youtube: false,
        reddit: false
      },
      platformsToAnalyse: {
        youtube: false,
        reddit: false
      },
      movieInfoToPull: {
        name: false,
        description: false,
        releaseDate: false,
        rating: false,
        providers: false,
        directors: false,
        endYear: 0,
        startYear: 0
      },
      movieIdToRemove: ''
    }
  },
  methods: {
    async pullComments() {
      console.log('@pullComments')
      await this.$store.dispatch('requestMovieNames')
      const movieNames = this.$store.getters.getMovieNames
      if (movieNames.length === 0) {
        alert('No movies in the database. Pull movies first.')
        return
      } else if (!this.platformsToPull.youtube && !this.platformsToPull.reddit) {
        alert('Select at least one platform to pull comments from.')
        return
      } else {
        for (const movie of movieNames) {
          setTimeout(async () => {
            const movieData = {
              movie: {
                movieName: movie.movieName
              },
              platform: {
                youtube: this.platformsToPull.youtube,
                reddit: this.platformsToPull.reddit
              }
            }
            await this.$store.dispatch('pullComments', movieData)
          }, 2000)
        }
      }
    },
    async analyseSentiment() {
      if (!this.platformsToAnalyse.youtube && !this.platformsToAnalyse.reddit) {
        alert('Select at least one platform to pull comments from.')
        return
      } else {
        await this.$store.dispatch('requestMovieNames')
        const movieNames = this.$store.getters.getMovieNames

        let counter = 0

        const intervalId = setInterval(async () => {
          const movie = movieNames[counter]

          if (movie) {
            const platformData = {
              is_youtube: this.platformsToAnalyse.youtube,
              is_reddit: this.platformsToAnalyse.reddit,
              movieNames: movie
            }

            await this.$store.dispatch('analyseSentiment', platformData)

            counter++
          } else {
            // If all movies have been processed, clear the interval
            clearInterval(intervalId)
          }
        }, 15000)
      }
    },

    pullMovies() {
      if (this.startYear > this.endYear) {
        alert('start year must be less than end year')
        return
      } else if (this.startYear < 1900 || this.endYear > 2023) {
        alert('start year must be greater than 1900 and end year must be less than 2021')
        return
      } else {
        const payload = {
          startYear: this.startYear,
          endYear: this.endYear
        }
        this.$store.dispatch('getDatabase', payload)
        // TODO: Implement pull movies functionality
      }
    },
    testPopDb() {
      this.$store.dispatch('testPopularDb')
    },
    removeAllComments() {
      // TODO: Implement remove all comments functionality
      this.$store.dispatch('removeAllComments')
    },
    removeDb(dbName) {
      this.$store.dispatch('removeDatabase', dbName)
    },
  }
}
</script>
