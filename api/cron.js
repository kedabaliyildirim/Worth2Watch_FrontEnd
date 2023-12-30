/* eslint-disable no-unused-vars */
import axios from 'axios';

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
        movie: movie
    };

    try {
        console.log("@pullComments");
        const response = await axios({
            url: localURL + "comments/pullcomments",
            method: "POST",
            data: data,
            withCredentials: true,
        });

        console.log("Comments pulled");
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
            url: localURL + "comments/getmovienames",
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