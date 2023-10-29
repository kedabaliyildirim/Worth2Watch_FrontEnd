export default {
    setMovieData(state, movieData) {
        state.movieData = movieData;
    },
    setCSRFToken(state, csrfToken) {
        state.csrfToken = csrfToken;
    },
    setAuthToken(state, authToken) {
        state.authToken = authToken;
    },
    setLoginState(state, loginState) {
        state.loginState = loginState;
    }
}