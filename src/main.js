import './assets/main.css';

import {
    createApp
} from 'vue';
import App from './App.vue';
import router from './router';
import store from "./store";

const app = createApp(App);

const createStore = async () => {
    await store.dispatch('getMovieData', {
        page: 1,
        page_size: 20
    });
    await store.dispatch('getTopTen');
};

app.use(router);
app.use(store);
createStore(); // Call the createStore function to dispatch the actions
app.mount('#app');
