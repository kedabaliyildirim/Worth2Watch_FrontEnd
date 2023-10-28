<template>
  <div class="mainBox">
    <div class="row" v-for="(movie, index) in movieStrings" :key="index">
      <div class="individualBox">
        <p class="releaseDate">{{ movie.movieReleaseDate }}</p>
        <img :src="movie.imageURL" alt="Movie Poster" class="poster" />
        <div class="details">
          <h3 class="movieName">{{ movie.movieName }}</h3>
          <p class="movieGenre">{{ movie.movieGenre }}</p>
          <div class="providers" v-if="movie.movieProviders !== 'No providers available'">
            <div
              v-for="provider in movie.movieProviders"
              :key="provider.provider_id"
              class="provider"
            >
              <img
                :src="
                  getProviderLogoPath('https://image.tmdb.org/t/p/original' + provider.logo_path)
                "
                alt="Provider Logo"
                class="providerLogo"
              />
              {{ provider.provider_name }}
            </div>
          </div>
          <p v-else style="margin-top: 4%">No providers available</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    movieStrings: {
      type: Array,
      required: true
    }
  },
  methods: {
    getProviderLogoPath(logoPath) {
      // You might need to adjust the base URL or handle null paths
      return `https://image.tmdb.org/t/p/original${logoPath}`
    }
  }
}
</script>

<style>

.mainBox {
  margin-top: 5%;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  width: 90%;
  background-color: #e6e7eb; /* Light gray background */
}

.row {
  display: flex;
  justify-content: center;
  margin: 10px 0;
}

.individualBox {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px;
  max-height: 450px; /* Adjust max height as needed */
  max-width: 300px; /* Adjust max width as needed */
  color: black;
  background-color: white;
  box-shadow: 22px 10px 10px rgba(0, 0, 0, 0.1);
  overflow: scroll;
}

.poster {
  max-width: 100%;
  max-height: 70%; /* Adjust max height of the poster */
  object-fit: cover; /* Ensure the image covers the entire container */
}
.movieGenre{
  font-weight: bold;
}
.details {
  padding: 10px;
  text-align: center;
  font-weight: bold;
}

.movieName {
  font-weight: bold;
  color: blue;
}

.releaseDate {
  align-self: flex-end;
  font-weight: bold;
  /* font-size: 1.8em; Adjust font size for release date */
}

.movieGenre {
  font-style: italic;
}

.providers {
  display: flex;
  margin-top: 10px;
  flex-wrap: wrap;
  object-fit: contain;
}

.providerLogo {
  max-width: 20px; /* Adjust max width of provider logo */
  margin-left: 10px;
}
</style>
