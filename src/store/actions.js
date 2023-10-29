/* eslint-disable no-unused-vars */
import axios from 'axios';
const url =
    import.meta.env.VITE_API_URL;


const localURL = 'http://127.0.0.1:8000/'

export default {
    setAuthToken(context, payload) {
        context.commit('setAuthToken', payload);
    },
    async authenticate(context, payload) {
        await axios({
            url: localURL + "getAuth",
            method: "post",
            withCredentials: true,
            data: payload
        }).then((response) => {
            if (response.data.status === "ok") {
                context.commit('setLoginState', true);
            } else {
                context.commit('setLoginState', false);
            }
        }).catch((error) => {
            console.error('Error in login request:', error);
        });
    },

    async getMovieData(context) {
        const payload = await axios({
            url: localURL + "allmovies",
            method: "GET"
        });
        context.commit('setMovieData', payload.data);
    },

    async login(context, payload) {
        const setCookies = (name, value, expirationDays = 1) => {
            const date = new Date();
            date.setTime(date.getTime() + (expirationDays * 24 * 60 * 60 * 1000));
            const cookieName = name + "=";
            let expires = "expires=" + date.toUTCString();
            document.cookie = cookieName + value + ";" + expires + ";path=/";
        }
        await axios({
            url: localURL + "mod/log",
            method: "POST",
            data: payload,
            withCredentials: true,
            headers: {
                'X-CSRFToken': context.state.csrfToken,
                'Content-Type': 'application/json', // Add this line
            }
        }).then((response) => {
            context.commit('setAuthToken', response.data.authToken);
            //set cookie here
            setCookies("authToken", response.data.authToken, 1);
        }).catch((error) => {
            console.error('Error in login request:', error);
        });
    },



}