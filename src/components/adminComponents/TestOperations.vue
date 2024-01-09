<template>
  <div class="adminContentHeader">
    <button @click="logout" class="logoutButton">Logout</button>
    <p>Admin Operations</p>
  </div>

  <!-- Testing Operations -->
  <div class="testingOperations">
    <h3>Testing Operations</h3>

    <!-- Content Database Test -->
    <div class="testOperation">
      <button
        @click="initializeContentDatabaseTest"
        :disabled="contentDatabaseTestStatus === 'ongoing'"
      >
        Initialize Database Test
      </button>
      <span class="statusIcon" :class="contentDatabaseTestStatus"></span>
    </div>

    <div class="testOperation">
      <button @click="checkEmptyComments">check and fill empty comments</button>
      <button disabled @click="checkEmptyYTComments">check and fill empty youtube</button>
    </div>
    <!-- Server Connection Test -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      // ... (previous data)
      contentDatabaseTestStatus: '', // ongoing, passed, failed
      adminDatabaseTestStatus: '', // ongoing, passed, failed
      commentDatabaseTestStatus: '', // ongoing, passed, failed
      serverConnectionTestStatus: '', // ongoing, passed, failed
      customTestStatus: '' // ongoing, passed, failed
    }
  },
  methods: {
    // ... (previous methods)

    async initializeContentDatabaseTest() {
      this.contentDatabaseTestStatus = 'ongoing'
      await this.$store.dispatch('testDb')
      const testResults = this.$store.getters.getTestResults
      const isPassed = (result) => result === true
      if (testResults.every(isPassed)) {
        this.contentDatabaseTestStatus = 'passed'
      } else {
        this.contentDatabaseTestStatus = 'failed'
      }
    },

    async checkEmptyComments() {
      await this.$store.dispatch('checkEmptyComments')
      const movieNames = this.$store.getters.getEmptyList
      for (const movie of movieNames) {
        console.log(movie)
        setTimeout(async () => {
          const movieData = {
            movie: {
              movieName: movie
            },
            platform: {
              youtube: true,
              reddit: true
            }
          }
          await this.$store.dispatch('pullComments', movieData)
        }, 2000)
      }
    },
    checkEmptyYTComments() {
      this.$store.dispatch('emptyYoutubeComments')
    }
  }
}
</script>
