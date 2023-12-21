export default {
    getMovies(state) {
        return state.movieData;
    },
    getLoginState(state) {
        return state.loginState;
    },
    getCsrftoken(state) {
        return state.csrfToken;
    },
    getAuthToken(state) {
        return state.authToken;
    },
    getCurrentMovie(state) {
        return state.currentMovie;
    },
    getSearchResults(state) {
        return state.searchResults;
    },
    getTotalPageCount(state) {
        return state.totalPageCount;
    },
    getTrailers(state) {
        return state.trailers;
    },
    getAdminList(state) {
        return state.adminList;
    },
    getTopTenMovies(state) {
        return state.topTenMovies;
    }
};