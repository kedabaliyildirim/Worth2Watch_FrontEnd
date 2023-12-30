<template>
  <div class="adminContentHeader">
    <button @click="logout" class="logoutButton">Logout</button>
    <p>Admin Operations</p>
  </div>

  <div class="adminContentBody">
    <!-- Register Admin Form -->
    <!-- ... (previous code) ... -->

    <!-- Pull Comments Form -->
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
      <label>Select information to pull:</label>
      <div disabled>
        <label>
          <input type="checkbox" v-model="movieInfoToPull.name" />
          Movie Name
        </label>
        <label>
          <input type="checkbox" v-model="movieInfoToPull.description" />
          Movie Description
        </label>
        <label>
          <input type="checkbox" v-model="movieInfoToPull.releaseDate" />
          Release Date
        </label>
        <label>
          <input type="checkbox" v-model="movieInfoToPull.rating" />
          Movie Rating
        </label>
        <label>
          <input type="checkbox" v-model="movieInfoToPull.providers" />
          Movie Providers
        </label>
        <label>
          <input type="checkbox" v-model="movieInfoToPull.directors" />
          Movie Directors
        </label>
      </div>
      <label for="PageNoToPulled">start yaer</label>
      <input class="PageNoToPulled" type="number" v-model="startYear" />
      <label for="PageNoToPulled">end year</label>
      <input class="PageNoToPulled" type="number" v-model="endYear" />
      <button @click="pullMovies">Pull Movies</button>
    </form>
    <button @click="testPopDb" class="logoutButton">Force pull top 10 movies</button>
    <!-- Admin Deletion Form -->
    <div class="dangerZone">
      <h3>Danger Zone</h3>
      <form @submit.prevent="removeAllComments">
        <button type="submit">Remove All Comments</button>
      </form>
      <form @submit.prevent>
        <button @click="removeAllMovies">Remove All Movies</button>
      </form>
      <form @submit.prevent="removeMovieById">
        <label for="movieIdToRemove">Remove Movie by ID:</label>
        <input type="text" v-bind="movieIdToRemove" required />
        <button type="submit">Remove Movie</button>
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
          const movieData = {
            movie: {
              movieName: movie.movieName,
            },
            platform: {
              youtube: this.platformsToPull.youtube,
              reddit: this.platformsToPull.reddit
            }
          }
          this.$store.dispatch('pullComments', movieData)
        }
      }
    },
    async analyseSentiment() {
      if (!this.platformsToAnalyse.youtube && !this.platformsToAnalyse.reddit) {
        alert('Select at least one platform to pull comments from.')
        return
      } else {
        const platformData = {
          youtube: this.platformsToAnalyse.youtube,
          reddit: this.platformsToAnalyse.reddit
        }
        this.$store.dispatch('analyseSentiment', platformData)
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
      console.log('Remove All Comments functionality')
    },
    removeAllMovies() {
      this.$store.dispatch('removeDatabase')
      console.log('Remove All Movies functionality')
    },
    removeMovieById() {
      // TODO: Implement remove movie by ID functionality
      console.log('Remove Movie by ID functionality', this.movieIdToRemove)
    }
  }
}
</script>
