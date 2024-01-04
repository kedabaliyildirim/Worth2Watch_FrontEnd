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
        Initialize Content Database Test
      </button>
      <span class="statusIcon" :class="contentDatabaseTestStatus"></span>
    </div>

    <!-- Admin Database Test -->
    <div class="testOperation">
      <button
        @click="initializeAdminDatabaseTest"
        :disabled="adminDatabaseTestStatus === 'ongoing'"
      >
        Initialize Admin Database Test
      </button>
      <span class="statusIcon" :class="adminDatabaseTestStatus"></span>
    </div>

    <!-- Comment Database Test -->
    <div class="testOperation">
      <button
        @click="initializeCommentDatabaseTest"
        :disabled="commentDatabaseTestStatus === 'ongoing'"
      >
        Initialize Comment Database Test
      </button>
      <span class="statusIcon" :class="commentDatabaseTestStatus"></span>
    </div>
    <div class="testOperation">
      <button @click="checkEmptyComments">check and fill empty comments</button>
      <button disabled @click="checkEmptyYTComments">check and fill empty youtube</button>
    </div>
    <!-- Server Connection Test -->
    <div class="testOperation">
      <button
        @click="initializeServerConnectionTest"
        :disabled="serverConnectionTestStatus === 'ongoing'"
      >
        Initialize Server Connection Test
      </button>
      <span class="statusIcon" :class="serverConnectionTestStatus"></span>
    </div>

    <!-- Custom Test (Adjust as needed) -->
    <div class="testOperation">
      <button @click="initializeCustomTest" :disabled="customTestStatus === 'ongoing'">
        Initialize Custom Test
      </button>
      <span class="statusIcon" :class="customTestStatus"></span>
    </div>
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
      customTestStatus: '', // ongoing, passed, failed
    };
  },
  methods: {
    // ... (previous methods)

    initializeContentDatabaseTest() {
      this.contentDatabaseTestStatus = 'ongoing';
      this.$store.dispatch('testDb')
      // TODO: Implement content database test logic
      // Set this.contentDatabaseTestStatus to 'passed' or 'failed' accordingly
      console.log('Content Database Test initialized');
    },

    initializeAdminDatabaseTest() {
      this.adminDatabaseTestStatus = 'ongoing';
      // TODO: Implement admin database test logic
      // Set this.adminDatabaseTestStatus to 'passed' or 'failed' accordingly
      console.log('Admin Database Test initialized');
    },

    initializeCommentDatabaseTest() {
      this.commentDatabaseTestStatus = 'ongoing';
      // TODO: Implement comment database test logic
      // Set this.commentDatabaseTestStatus to 'passed' or 'failed' accordingly
      console.log('Comment Database Test initialized');
    },

    initializeServerConnectionTest() {
      this.serverConnectionTestStatus = 'ongoing';
      // TODO: Implement server connection test logic
      // Set this.serverConnectionTestStatus to 'passed' or 'failed' accordingly
      console.log('Server Connection Test initialized');
    },

    initializeCustomTest() {
      this.customTestStatus = 'ongoing';
      // TODO: Implement custom test logic
      // Set this.customTestStatus to 'passed' or 'failed' accordingly
      console.log('Custom Test initialized');
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
  },
}
</script>