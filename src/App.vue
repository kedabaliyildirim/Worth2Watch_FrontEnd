<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <RouterView />
</template>
<script >
// eslint-disable-next-line no-unused-vars
import { RouterLink, RouterView } from 'vue-router'
// eslint-disable-next-line no-unused-vars
export default {
  created() {
    this.$store.dispatch('getMovieData')
  }
}
</script>

<style scoped>

</style>
