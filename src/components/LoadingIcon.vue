<template>
    <div class="loading-container" :class="{ 'html-blur': loading }">
      <div class="background-overlay"></div>
      <div class="loader">
        <div class="box-load1"></div>
        <div class="box-load2"></div>
        <div class="box-load3"></div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      loading: Boolean,
    },
    methods: {
      addBlurClass() {
        document.documentElement.classList.add('html-blur');
      },
      removeBlurClass() {
        document.documentElement.classList.remove('html-blur');
      },
    },
    watch: {
      loading(newVal) {
        if (newVal) {
          this.addBlurClass();
        } else {
          this.removeBlurClass();
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .loading-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000; /* Higher z-index to place on top of the background */
  }
  
  .background-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #0c1821;
    /* background-color: #0c0d28;  */
    opacity: 1; /* Adjust the opacity as needed */
    z-index: 998; /* Lower z-index to place behind the loader */
  }
  
  .loader {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 10vh;
    position: relative;
    z-index: 999; /* Higher z-index to place on top of the background */
  }
  
  .box-load1,
  .box-load2,
  .box-load3 {
    width: 12px;
    height: 12px;
    background-color: #ccc;
    margin: 0 3px;
    border-radius: 50%;
    animation: bounce 0.6s infinite alternate;
  }
  
  .box-load2 {
    animation-delay: 0.2s;
  }
  
  .box-load3 {
    animation-delay: 0.4s;
  }
  
  @keyframes bounce {
    to {
      transform: translateY(-8px);
    }
  }
  
  .html-blur {
    overflow: hidden; /* Prevent scrollbars */
  }
  </style>
  