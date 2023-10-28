/* eslint-disable no-unused-vars */
import axios from 'axios';
const url =import.meta.env.VITE_API_URL;


const localURL = url

export default {
    async authenticate(context) {
        // Get the CSRF token from the cookie

        // Set the CSRF token in the default headers for Axios

        // You can also check if the token is set correctly

        // Now you can make other Axios requests

    },

    async getMovieData(context) {
        const payload = await axios({
            url: localURL + "allmovies",
            method: "GET"
        });
        context.commit('setMovieData', payload.data);
    },

    async login(context, payload) {
        console.log("@action ");

        try {
            // First, make a request to get the CSRF token
            const csrfResponse = await axios.get(localURL + 'auth');

            console.log(csrfResponse.data.csrfToken);
            const loginResponse = await axios.post(
                localURL + 'admin/login',
                payload, {
                    withCredentials: true,
                    headers: {
                        'X-CSRFToken': csrfResponse.data.csrfToken,
                    },
                }
            );

            console.log(loginResponse.data);
            // handle successful response here

        } catch (error) {
            console.log(error);
            // handle error here
        }
    }

}