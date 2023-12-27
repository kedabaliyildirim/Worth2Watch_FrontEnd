<!-- EMRAH -->

<template>
  <div class="MoviePageMain">
    <div class="MoviePagePoster">
      <h1 class="movieTitle">{{ movieObj.movieName }}</h1>
      <ul class="movieScoreList">
        <li v-for="rating in movieObj.movieScore" :key="rating.Source">
          <strong>{{ rating.Source }}</strong> - {{ rating.Value }}
        </li>
      </ul>
      <img
        class="moviePoster"
        :src="movieObj.imageURL"
        :alt="movieObj.movieName + 'Movie Poster'"
      />
    </div>
    <div class="MoviePageDetails">
      <div class="sectionHeader">
        <h2 class="trailerHeader">Movie Trailer</h2>
      </div>
      <div class="trailerContainer">
        <iframe
          class="movieTrailer"
          width="100%"
          height="315"
          :src="trailer"
          title="YouTube video player"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowfullscreen
        ></iframe>
      </div>
      <div class="sectionHeader">
        <h2 class="detailsHeader">Movie Details</h2>
      </div>
      <div class="detailsContainer">
        <p>
          <strong class="movieDetailLabel">Release Date:</strong> {{ movieObj.movieReleaseDate }}
        </p>
        <p><strong class="movieDetailLabel">Genre:</strong> {{ movieObj.movieGenre }}</p>
        <p><strong class="movieDetailLabel">Duration:</strong> {{ movieObj.movieDuration }}</p>
        <p><strong class="movieDetailLabel">Director:</strong> {{ movieObj.movieDirector }}</p>
        <p><strong class="movieDetailLabel">Writer:</strong> {{ movieObj.movieWriter }}</p>
        <p><strong class="movieDetailLabel">Actors:</strong> {{ movieObj.movieActors }}</p>
      </div>
      <div class="sectionHeader">
        <h2 class="detailsHeader">Description</h2>
      </div>
      <div class="detailsContainer">
        <p class="movieDescription">{{ movieObj.description }}</p>
      </div>
      <div class="commentSection">
        <div class="commentBody">
            <h3>Youtube comments</h3>
        </div>
        <div class="commentBody">
            <h3>Reddit Comments</h3>
        </div>
        <div class="commentBody">
            <h3>Custom comments</h3>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: ['movieObj'],
  created() {
    this.$store.dispatch('getTrailer', this.movieObj.movieName)
  },
  computed: {
    trailer() {
      // Use optional chaining to handle potential null or undefined
      const preURL = this.$store.getters.getTrailers

      // Check if preURL is a string before using the replace method
      if (typeof preURL === 'string') {
        const mainURL = `https://www.youtube.com/embed/${preURL.replace(
          'https://www.youtube.com/watch?v=',
          ''
        )}`
        return mainURL
      } else {
        return '' // or a default URL if preURL is not a string
      }
    }
  }
}
</script>
