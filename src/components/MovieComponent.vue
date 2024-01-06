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

      <div class="provider-container">
        <img
          v-for="provider in movieObj.movieProviders"
          :key="provider.provider_id"
          :src="getProviderLogoPath('https://image.tmdb.org/t/p/original' + provider.logo_path)"
          style="max-width: 25px"
          alt="Provider Logo"
        />
      </div>
      <div class="detailsContainer-2">
        <!-- nereden izleyebilirsiniz? -->

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

      <!-- Reddit start -->
      <div class="commentSection">
        <div class="faq-container">
          <div class="faq-question-2" @click="toggleFAQ2">
            <img
              style="width: 18px; margin-left: 15px"
              src="@/assets/icons/toogle.svg"
              alt="My Icon"
            />
            <div>
              <img
                style="width: 25px; margin-bottom: -7px"
                src="@/assets/icons/reddit.png"
                alt="My Icon"
              />
              <span> Reddit Comments</span>
            </div>

            <p class="sentiment-analyze" ref="redditSentiment"></p>
          </div>
          <!-- Updated loop to create faq-answer-2 only if sentiment is present -->
          <template v-for="(comment, index) in movieObj.movieComments.redditComments" :key="index">
            <template v-if="comment.sentiment !== undefined">
              <div class="faq-answer-2">
                {{ comment.comment }}
                <div class="left-aligned">{{ comment.sentiment }}</div>
              </div>
            </template>
          </template>
        </div>
      </div>
      <!-- Reddit finish -->

      <!-- youtube start -->
      <!-- 
      <div class="commentSection">
        <div class="faq-container">
          <div class="faq-question" @click="toggleFAQ2">
            <img
              style="width: 18px; margin-left: 15px"
              src="@/assets/icons/toogle.svg"
              alt="My Icon"
            />
            YouTube Comments
            <p class="sentiment-analyze" ref="youtubeSentiment"></p>
          </div>

          <template v-for="(comment, index) in movieObj.movieComments.youtubeComments" :key="index">
            <template v-if="comment.sentiment !== undefined">
              <div class="faq-answer">
                {{ comment.comment }}
                <div class="left-aligned">{{ comment.sentiment }}</div>
              </div>
            </template>
          </template>
        </div>
      </div> -->

      <!-- youtube finish -->
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

    // toggleFAQ1() {
    //   var answers = document.getElementsByClassName('faq-answer')
    //   for (var i = 0; i < answers.length; i++) {
    //     if (answers[i].style.display === 'none') {
    //       answers[i].style.display = 'block'
    //     } else {
    //       answers[i].style.display = 'none'
    //     }
    //   }

    //   // Comment sentimenterini toplamak ve ortalama hesaplamak için
    //   const sentimentList = this.movieObj.movieComments.youtubeComments
    //     .filter((comment) => comment.sentiment !== undefined) // Filter out comments without sentiment
    //     .map((comment) => comment.sentiment)

    //   const totalSentiments = sentimentList.length
    //   const sumOfSentiments = sentimentList.reduce(
    //     (sum, sentiment) => sum + parseFloat(sentiment),
    //     0
    //   )

    //   // Check if there are comments with sentiment to avoid division by zero
    //   const averageSentiment = totalSentiments > 0 ? sumOfSentiments / totalSentiments : 0

    //   this.$refs.youtubeSentiment.innerHTML = `<span style="color: #ccc9dc; border: 1px solid #8ea7e9; font-weight:bold; border-radius: 50%; padding: 7px">${averageSentiment.toFixed(
    //     2
    //   )}</span>`
    // },
    toggleFAQ2() {
      var answers = document.getElementsByClassName('faq-answer-2')
      for (var i = 0; i < answers.length; i++) {
        if (answers[i].style.display === 'none') {
          answers[i].style.display = 'block'
        } else {
          answers[i].style.display = 'none'
        }
      }

      // Comment sentimenterini toplamak ve ortalama hesaplamak için
      const sentimentList = this.movieObj.movieComments.redditComments
        .filter((comment) => comment.sentiment !== undefined) // Filter out comments without sentiment
        .map((comment) => comment.sentiment)

      const totalSentiments = sentimentList.length
      const sumOfSentiments = sentimentList.reduce(
        (sum, sentiment) => sum + parseFloat(sentiment),
        0
      )

      // Check if there are comments with sentiment to avoid division by zero
      const averageSentiment = totalSentiments > 0 ? sumOfSentiments / totalSentiments : 0

      this.$refs.redditSentiment.innerHTML = `<span style="color: #ccc9dc; border: 1px solid #8ea7e9; font-weight:bold; border-radius: 50%; padding: 7px">${averageSentiment.toFixed(
        2
      )}</span>`
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
  display: flex;
  flex-direction: row;
  justify-content: space-between;
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

.left-aligned {
  float: right;
  margin-top: 0.5%;
  margin-left: 5%;
  border-radius: 50%;
  color: #d1b47a;
  font-weight: bold;
}
.sentiment-analyze {
  color: #ccc9cc;
  margin-right: 20px;
}

.provider-container {
  display: flex;
  gap: 10px;
  align-items: center;
}
</style>
