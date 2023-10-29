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
    }
}