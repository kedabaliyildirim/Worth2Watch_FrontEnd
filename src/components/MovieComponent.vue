<template>
  <div class="MoviePageMain">
    <div class="Headline">
      <p class="movieTitle">{{ movieObj.movieName }}</p>
      <p class="movieDuration">{{ movieObj.movieDuration }}</p>
    </div>
    <hr style="margin-top: 5px; width: 100%" class="custom-line" />
    <br />
    <div>
      <div class="MoviePagePoster">
        <img
          class="moviePoster"
          :src="movieObj.imageURL"
          :alt="movieObj.movieName + 'Movie Poster'"
        />
      </div>
      <!-- detail -->
      <div class="detailsContainer-2">
        <!-- nereden izleyebilirsiniz? -->
        <div v-for="provider in movieObj.movieProviders" :key="provider.provider_id" class="provider">
          <img
            :src="getProviderLogoPath('https://image.tmdb.org/t/p/original' + provider.logo_path)"
            style="max-width: 22px"
            alt="Provider Logo"
            class="providerLogo"
          />
        </div>

        <div class="description-4">
          <p class="movieGenre">{{ movieObj.movieGenre }}</p>
        </div>

        <p>
          <strong style="color: #fff5ee; margin-right: 8px" class="movieDetailLabel"
            >Release Date:</strong
          >
          {{ formatDate(movieObj.movieReleaseDate) }}
        </p>
        <hr class="custom-line-2" />

        <p>
          <strong style="color: #fff5ee; margin-right: 8px" class="movieDetailLabel"
            >Director:</strong
          >
          {{ movieObj.movieDirector }}
        </p>
        <hr class="custom-line-2" />

        <p>
          <strong style="color: #fff5ee; margin-right: 8px" class="movieDetailLabel"
            >Actors:</strong
          >
          {{ movieObj.movieActors }}
        </p>
        <hr class="custom-line-2" />
      </div>
      <!-- alt -->
      <div class="star">
        <img style="width: 75%; height: 75%" src="@/assets/icons/star.png" alt="My Icon" />

        <ul class="movieScoreList">
          <li v-for="rating in movieObj.movieScore" :key="rating.Source">
            <strong>{{ rating.Source }}</strong> - {{ rating.Value }}
          </li>
        </ul>
      </div>
    </div>

    <div style="margin-bottom: 50px" class="MoviePageDetails">
      <div class="sectionHeader">
        <h2 style="margin-top: 50px" class="detailsHeader">Description</h2>
      </div>
      <div class="detailsContainer">
        <p class="movieDescription"><strong> ✨ </strong>{{ movieObj.description }}</p>
      </div>

      <!-- Youtube start -->
      <div class="commentSection">
        <div class="faq-container">
          <div class="faq-question" @click="toggleFAQ1">
            <img
              style="width: 18px; margin-left: 15px"
              src="@/assets/icons/toogle.svg"
              alt="My Icon"
            />
            YouTube Comments
            <p class="sentiment-analyze">👍% 52 - 💩 % 48</p>
            <!-- sentiment analiz -->
          </div>
          <div
            class="faq-answer"
            v-for="comment in movieObj.movieComments.youtubeComments"
            :key="comment"
          >
            {{ comment.comment }}
          </div>
        </div>
      </div>
      <!-- Youtube finish -->

      <!-- reddit-start -->
      <div class="commentSection">
        <div class="faq-container">
          <div class="faq-question-2" @click="toggleFAQ2">
            <img
              style="width: 18px; margin-left: 15px"
              src="@/assets/icons/toogle.svg"
              alt="My Icon"
            />
            Reddit Comments
            <p class="sentiment-analyze">👍% 61 - 💩 % 39</p>
            <!-- sentiment analiz -->
          </div>
          <div
            class="faq-answer-2"
            v-for="comment in movieObj.movieComments.redditComments"
            :key="comment"
          >
            {{ comment.comment }}
            {{ comment.sentiment }}
          </div>
        </div>
      </div>
      <!-- Reddit finish -->
    </div>
  </div>
</template>

<script>
export default {
  props: ['movieObj'],
  methods: {
    getProviderLogoPath(logoPath) {
      return `https://image.tmdb.org/t/p/original${logoPath}`
    },
    toggleFAQ1() {
      var answers = document.getElementsByClassName('faq-answer')
      for (var i = 0; i < answers.length; i++) {
        if (answers[i].style.display === 'none') {
          answers[i].style.display = 'block'
        } else {
          answers[i].style.display = 'none'
        }
      }
    },
    toggleFAQ2() {
      var answers = document.getElementsByClassName('faq-answer-2')
      for (var i = 0; i < answers.length; i++) {
        if (answers[i].style.display === 'none') {
          answers[i].style.display = 'block'
        } else {
          answers[i].style.display = 'none'
        }
      }
    },
    formatDate(value) {
      const options = { day: 'numeric', month: 'short', year: 'numeric' }
      const date = new Date(value)
      return date.toLocaleDateString('en-GB', options)
    }
  }
}
</script>

<style>
.faq-container {
  width: 100%;
}

.faq-question {
  display: flex;
  padding: 1%;
  background-color: #32302c;
  margin-top: 3%;
  margin-bottom: 3px;
  border-radius: 30px;
  border: #209596 solid 1px;
  max-width: 100%;
  cursor: pointer;
  justify-content: space-between;
  color: #fffae8;
}

.faq-answer {
  display: none;
  padding: 5px;
  padding-left: 3%;
  padding-right: 3%;
  background-color: #32302c;
  margin-bottom: 3px;
  border-radius: 30px;
  border: #209596 solid 1px;
  width: 90%;
  margin-left: 5%;
  color: #ccc9cc;
}

.faq-question-2 {
  display: flex;
  padding: 1%;
  background-color: #32302c;
  margin-top: 3%;
  margin-bottom: 3px;
  border-radius: 30px;
  border: 1px solid #8ea7e9;
  max-width: 100%;
  cursor: pointer;
  justify-content: space-between;
  color: #fffae8;
}

.faq-answer-2 {
  display: none;
  padding: 5px;
  padding-left: 3%;
  padding-right: 3%;
  background-color: #32302c;
  margin-bottom: 3px;
  border-radius: 30px;
  border: 1px solid #8ea7e9;
  width: 90%;
  margin-left: 5%;
  color: #ccc9cc;
}
.sentiment-analyze {
  color: #ccc9cc;
  margin-right: 20px;
}
</style>
