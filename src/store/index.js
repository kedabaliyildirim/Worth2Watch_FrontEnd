import actions from './actions';
import mutations from './mutations';
import getters from './getters';
import {
    createStore
} from "vuex";
const store = createStore({
    state: {
        movieData: [],
    },
    actions,
    mutations,
    getters
});

export default store;