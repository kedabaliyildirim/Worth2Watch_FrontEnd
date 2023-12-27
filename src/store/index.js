/* jshint esversion: 6 */
import actions from './actions';
import mutations from './mutations';
import getters from './getters';
import {
    createStore
} from "vuex";
const store = createStore({
    state: {
        movieData: [],
        loginState: false,
        csrfToken: null,
        authToken: null,
        isLogged: false,
        currentMovie: {},
        searchResults: [],
        totalPageCount: 0,
        trailers: [],
        adminList: [],
        topTenMovies: [],
        movieNames: [],
    },
    actions,
    mutations,
    getters
});

export default store;