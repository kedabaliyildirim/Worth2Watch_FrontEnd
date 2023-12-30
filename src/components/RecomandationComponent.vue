
<template>
  <h2 id="headline">Top 10 Movies</h2>
  <div class="mainBox">
    <div class="row-2" v-for="(movie, index) in movieStrings" :key="index">
      <router-link :to="{ name: 'movie', params: { id: movie.movie_id } }">
        <!-- card -->
        <div class="card">
          <div class="content">
            <div class="back">
              <div class="back-content">
                <img
                  :src="movie.imageURL"
                  :alt="movie.movieName + ' Movie Poster'"
                  class="poster-2 lazyload"
                />
              </div>
            </div>
            <div class="front">
              <div class="front-content">
                <small class="badge">{{ movie.movieName }}</small>
                <div class="description">
                  <div class="title">
                    <p class="title">{{ movie.movieRuntime}} </p>
                  </div>
                  <p class="card-footer">{{ movie.movieReleaseDate }} &nbsp;</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </router-link>
    </div>
  </div>
  <hr class="custom-line" />
</template>

<script>
export default {
  computed: {
    movieStrings() {
      const movieObject = this.$store.getters.getTopTenMovies
      let provider = ''
      return movieObject.map((movie) => {
        try {
          const parsedMovie = JSON.parse(movie)
          if (parsedMovie.movieProvider && parsedMovie.movieProvider.US) {
            provider = parsedMovie.movieProvider.US
          } else {
            provider = 'No providers available'
          }
          return {
            movieName: parsedMovie.movieName,
            movieReleaseDate: parsedMovie.movieReleaseDate,
            movieGenre: parsedMovie.movieGenres,
            imageURL: parsedMovie.imageURL,
            movieProviders: provider,
            movie_id: parsedMovie._id.$oid,

            movieRuntime: parsedMovie.movieRuntime
          }
        } catch (error) {
          console.log(error)
        }
      })
    }
  }
}
</script>

<style>

.card {
  overflow: visible;
  width: 105px;
  height: 175px;
  color: #ccc9dc;
  margin-right: 7px;
}

.content {
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transition: transform 300ms;
  box-shadow: 0px 0px 10px 1px #000000;
  border-radius: 5px;
}

.front,
.back {
  background-color: #151515;
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  border-radius: 5px;
  overflow: hidden;
}

.back {
  width: 100%;
  height: 100%;
  justify-content: center;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.back::before {
  position: absolute;
  content: ' ';
  display: block;
  width: 160px;
  height: 160%;
  background: linear-gradient(90deg, transparent, #008000, #ccc9dc, transparent);
  animation: rotation_481 5000ms infinite linear;
}

.back-content {
  position: absolute;
  width: 99%;
  height: 99%;
  background-color: #151515;
  border-radius: 5px;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 30px;
}

.card:hover .content {
  transform: rotateY(180deg);
}

@keyframes rotation_481 {
  0% {
    transform: rotateZ(0deg);
  }

  0% {
    transform: rotateZ(360deg);
  }
}

.front {
  transform: rotateY(180deg);
  color: white;
}

.front .front-content {
  background-color: #1b2a41;
  position: absolute;
  width: 100%;
  height: 100%;
  padding: 8px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.front-content .badge {
  background-color: #00000099;
  padding: 2px 10px;
  border-radius: 10px;
  backdrop-filter: blur(2px);
  width: fit-content;
  font-size: 12px;
  border: 1px dashed white;
}

.description {
  width: 100%;
  padding: 10px;
  background-color: #00000099;
  backdrop-filter: blur(5px);
  border-radius: 10px;
}

.title {
  font-size: 10px;
  max-width: 100%;
  display: flex;
}

.title p {
  width: 100%;
  font-size: 10px;
}

.card-footer {
  color: #ffffff88;
  margin-top: 5px;
  font-size: 8px;
}

@keyframes floating {
  0% {
    transform: translateY(0px);
  }

  50% {
    transform: translateY(10px);
  }

  100% {
    transform: translateY(0px);
  }
}
</style>
