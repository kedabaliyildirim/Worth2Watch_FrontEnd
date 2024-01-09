export default {
    setMovieData(state, movieData) {
        state.movieData = movieData;
    },
    setTotalPageCount(state, totalPageCount) {
        state.totalPageCount = totalPageCount;
    },
    clearMovieData(state) {
        state.movieData = [];
    },
    setCSRFToken(state, csrfToken) {
        state.csrfToken = csrfToken;
    },
    setAuthToken(state, authToken) {
        state.authToken = authToken;
    },
    setLoginState(state, loginState) {
        state.loginState = loginState;
    },
    setCurrentMovie(state, movie) {
        state.currentMovie = movie;
    },
    emptySearchResults(state) {
        state.searchResults = [];
    },
    setSearchResults(state, searchResults) {
        state.searchResults = searchResults;
    },
    setTrailers(state, trailers) {
        state.trailers = trailers;
    },
    setAdminList(state, adminList) {
        state.adminList = adminList;
    },
    setTopTenMovies(state, topTenMovies) {
        state.topTenMovies = topTenMovies;
    },
    setMovieNames(state, movieNames) {
        state.movieNames = movieNames;
    },
    setEmptyList(state, emptyList) {
        state.emptyList = emptyList
    },
    emptyState(state) {
        state.searchResults = [];
    },
    setTestResults(state, testResults) {
        state.testResults = testResults;
    }
};