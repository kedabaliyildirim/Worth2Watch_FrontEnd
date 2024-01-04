/* eslint-disable no-undef */
/* eslint-disable no-unused-vars */
const axios = require('axios');

// jshint ignore:start
let url;
let authKey
url = process.env.VITE_API_URL
authKey = process.env.VITE_AUTH_TOKEN
// jshint ignore:end
const localURL = url;
const pullComments = async (authCookie, movie) => {
    const data = {
        authToken: authCookie,
        platform: {
            "reddit": false,
            "youtube": true,
        },
        movie: {
            movieName:movie
        }
    };

    try {
        console.log("@pullComments ", movie);
        const response = await axios({
            url: localURL + "comments/pullcomments",
            method: "POST",
            data: data,
            withCredentials: true,
        });

        console.log("Comments pulled");
        if (response.data.error) {
            console.log("Error in pulling comments: ", response.data.error);
        }
    } catch (error) {
        console.error('Error in pullComments request:', error);
    }
};
const requestMovieNames = async (authCookie) => {
    const data = {
        authToken: authCookie
    };

    try {
        console.log("@requestMovieNames");
        const response = await axios({
            url: localURL + "mod/emptyyoutubecomments",
            method: "POST",
            data: data,
            withCredentials: true,
        });

        const movieNames = response.data;
        return movieNames;
    } catch (error) {
        console.error('Error in requestMovieNames request:', error);
        throw error; // Rethrow the error to handle it in the calling function
    }
};
const cron_main = async () => {
    try {
        console.log("Cron job started");
        console.log(localURL);
        const movieNames = await requestMovieNames(authKey);
        setTimeout(async () => {
            for (const movie of movieNames) {
                console.log(`Processing movie: ${movie}`);
                await pullComments(authKey, movie);
            }
        }, 2000);

        console.log("Cron job completed successfully");
    } catch (error) {
        console.error('Error in cron_main:', error);
    }
};

cron_main(); // Call the cron_main function to execute the cron job
