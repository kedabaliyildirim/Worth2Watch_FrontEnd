/* eslint-disable no-unused-vars */
import axios from 'axios';
import './getters.js';
// jshint ignore:start
let url;
const googleUrl =
    import.meta.env.VITE_GOOGLE_SEARCH_URI
const googleApiKey =
    import.meta.env.VITE_GOOGLE_API_KEY
url =
    import.meta.env.VITE_API_URL
// jshint ignore:end

const localURL = url;
//  const localURL = 'http://127.0.0.1:8000/';

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

    async getMovieData(context, payload) {


        // Clear existing movie data
        context.commit('clearMovieData');

        // Fetch total page count
        await axios({
            url: localURL + 'totalpages',
            method: "GET"
        }).then((response) => {
            context.commit('setTotalPageCount', response.data);
        }).catch((error) => {
            console.error('Error in login request:', error);
        });

        // Fetch new movie data
        await axios({
            url: localURL + 'allmovies',
            method: "POST",
            data: payload,
            withCredentials: true,
            headers: {
                'X-CSRFToken': context.state.csrfToken,
                'Content-Type': 'application/json', // Add this line
            }
        }).then((response) => {
            context.commit('setMovieData', response.data);
            return response;
        }).catch((error) => {
            console.error('Error in login request:', error);
        });
    },

    async login(context, payload) {
        const setCookies = (name, value, expirationDays = 1) => {
            const date = new Date();
            date.setTime(date.getTime() + (expirationDays * 24 * 60 * 60 * 1000));
            const cookieName = name + "=";
            let expires = "expires=" + date.toUTCString();
            document.cookie = cookieName + value + ";" + expires + ";path=/";
        };
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
    //Searches for a movie by name and returns the movie object to set as the current movie
    async searchMovie(context, payload) {
        await axios({
            url: localURL + "movies/search",
            method: "POST",
            data: payload,
            withCredentials: true,
            headers: {
                'X-CSRFToken': context.state.csrfToken,
                'Content-Type': 'application/json', // Add this line
            }
        }).then((response) => {
            context.commit('setSearchResults', response.data);
        }).catch((error) => {
            console.error('Error in request:', error);
        });
    },

    //Setting current movie to be displayed
    async setMovie(context, payload) {
        // if logged in add auth token from cookies and make a request to server with
        // payload to pull movie to database 
        await axios({
            url: localURL + "movies/getmovie",
            method: "POST",
            data: payload,
            withCredentials: true,
            headers: {
                'X-CSRFToken': context.state.csrfToken,
                'Content-Type': 'application/json', // Add this line
            }
        }).then((response) => {
            context.commit('setCurrentMovie', response.data);
        }).catch((error) => {
            console.error('Error in login request:', error);
        });
    },


    async getDatabase(context, payload) {
        let authCookie = null;
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${'authToken'}=`);
        if (parts.length === 2) {
            authCookie = parts.pop().split(';').shift();

            const startYear = payload.startYear;
            const endYear = payload.endYear;
            const data = {
                authToken: authCookie,
                startYear: startYear,
                endYear: endYear
            };
            await axios({
                url: localURL + "mod/pullcontent",
                method: "POST",
                data: data,
                withCredentials: true,
                headers: {
                    'X-CSRFToken': context.state.csrfToken,
                    'Content-Type': 'application/json', // Add this line
                }
            }).then((response) => {
                console.log(response.data);
            }).catch((error) => {
                console.error('Error in login request:', error);
            });
        } else {
            alert("You are not logged in");
            authCookie = null;
        }
    },

    removeDatabase(context, payload) {
        let authCookie = null;
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${'authToken'}=`);
        if (parts.length === 2) {
            authCookie = parts.pop().split(';').shift();
            const data = {
                authToken: authCookie,
                databaseName: payload
            }
            axios({
                url: localURL + "mod/dropdatabase",
                method: "POST",
                data: data,
                withCredentials: true,
                headers: {
                    'X-CSRFToken': context.state.csrfToken,
                    'Content-Type': 'application/json', // Add this line
                }
            }).then((response) => {
                console.log(response.data);
            }).catch((error) => {
                console.error('Error in login request:', error);
            });
        } else {
            alert("You are not logged in");
            authCookie = null;
        }
    },
    async getTrailer(context, payload) {
        try {
            const movieTitle = payload; // Assuming the payload is the movie name
            const maxResults = 1; // Assuming you want only one result
            const apiUrl = `${googleUrl}?q=${encodeURIComponent(movieTitle + ' trailer')}&type=video&key=${googleApiKey}&maxResults=${maxResults}`;

            const response = await axios.get(apiUrl);

            console.log(response.data);

            // Do something with the response, like extracting the video ID or URL
            const videoId = response.data.items[0].id.videoId;
            const trailerUrl = `https://www.youtube.com/watch?v=${videoId}`;
            context.commit('setTrailers', trailerUrl);

        } catch (error) {
            context.commit('setTrailers', error.data);

            console.error('Error in trailer request:', error);
        }
    },
    // async getTrailer(context, payload) {
    //     try {
    //         const movieTitle = payload; // Assuming the payload is the movie name
    //         const maxResults = 1; // Assuming you want only one result
    //         const apiUrl = `${googleUrl}?q=${encodeURIComponent(movieTitle + ' trailer')}&type=video&key=${googleApiKey}&maxResults=${maxResults}`;

    //         // Simulate an asynchronous operation with setTimeout
    //         setTimeout(async () => {
    //             try {
    //                 // Instead of making an actual API request, use mock data
    //                 const mockData = {
    //                     data: {
    //                         items: [{
    //                             id: {
    //                                 videoId: 'ib8fl7KrUC4'
    //                             },
    //                         }, ],
    //                     },
    //                 };

    //                 // Simulate the response handling
    //                 console.log(mockData.data);

    //                 // Do something with the mock response, like extracting the video ID or URL
    //                 const videoId = mockData.data.items[0].id.videoId;
    //                 const trailerUrl = `https://www.youtube.com/watch?v=${videoId}`;
    //                 console.log('Trailer URL:', trailerUrl);

    //                 // Update the state with the mock trailer URL
    //                 context.commit('setTrailers', trailerUrl);
    //             } catch (error) {
    //                 // Handle any error during the mock response handling
    //                 console.error('Error in mock response handling:', error);
    //             }
    //         }, 1000); // Simulate a delay of 1000 milliseconds (1 second)
    //     } catch (error) {
    //         // Handle any error during the simulated asynchronous operation
    //         context.commit('setTrailers', error);
    //         console.error('Error in trailer request:', error);
    //     }
    // },
    /* jshint ignore:start */
    async createCSV(context) {
        await axios({
            url: localURL + "mod/createcsv",
            method: "GET",
        }).then((response) => {
            console.log(response.data);
        }).catch((error) => {
            console.error('Error in login request:', error);
        });
    },
    /* jshint ignore:end */

    async createAdmin(context, payload) {
        let authCookie = null;
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${'authToken'}=`);
        if (parts.length === 2) {
            authCookie = parts.pop().split(';').shift();
            const data = {
                email: payload.email,
                password: payload.password,
                authToken: authCookie
            };
            axios({
                url: localURL + "mod/createadmin",
                method: "POST",
                data: data,
                withCredentials: true,
                headers: {
                    'X-CSRFToken': context.state.csrfToken,
                    'Content-Type': 'application/json', // Add this line
                }
            }).then((response) => {
                console.log("Admin created");
                console.log(response.data);
            }).catch((error) => {
                console.error('Error in login request:', error);
            });
        } else {
            alert("You are not logged in");
        }
    },

    async getAdmins(context) {
        let authCookie = null;
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${'authToken'}=`);
        if (parts.length === 2) {
            authCookie = parts.pop().split(';').shift();
            const data = {
                authToken: authCookie
            };
            axios({
                url: localURL + "mod/getadmins",
                method: "POST",
                data: data,
                withCredentials: true,
                headers: {
                    'X-CSRFToken': context.state.csrfToken,
                    'Content-Type': 'application/json', // Add this line
                }
            }).then((response) => {
                console.log("Admins fetched");
                console.log(response.data);
                context.commit('setAdminList', response.data);
            }).catch((error) => {
                console.error('Error in login request:', error);
            });
        } else {
            alert("You are not logged in");
        }

    },

    async deleteAdmin(context, payload) {
        let authCookie = null;
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${'authToken'}=`);
        if (parts.length === 2) {
            authCookie = parts.pop().split(';').shift();
            const data = {
                email: payload,
                authToken: authCookie
            };
            axios({
                url: localURL + "mod/deleteadmin",
                method: "POST",
                data: data,
                withCredentials: true,
                headers: {
                    'X-CSRFToken': context.state.csrfToken,
                    'Content-Type': 'application/json', // Add this line
                }
            }).then((response) => {
                console.log("Admin deleted");
                console.log(response.data);
            }).catch((error) => {
                console.error('Error in login request:', error);
            });
        } else {
            alert("You are not logged in");
        }
    },

    async changePassword(context, payload) {
        let authCookie = null;
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${'authToken'}=`);
        if (parts.length === 2) {
            authCookie = parts.pop().split(';').shift();
            const data = {
                email: payload.email,
                password: payload.password,
                authToken: authCookie
            };
            axios({
                url: localURL + "mod/changeadminpassword",
                method: "POST",
                data: data,
                withCredentials: true,
                headers: {
                    'X-CSRFToken': context.state.csrfToken,
                    'Content-Type': 'application/json', // Add this line
                }
            }).then((response) => {
                console.log("Password changed");
            }).catch((error) => {
                console.error('Error in login request:', error);
            });
        } else {
            alert("You are not logged in");
        }
    },

    getTopTen(context) {
        axios({
            url: localURL + "movies/topten",
            method: "GET",
            withCredentials: true,
            headers: {
                'X-CSRFToken': context.state.csrfToken,
                'Content-Type': 'application/json', // Add this line
            }
        }).then((response) => {
            context.commit('setTopTenMovies', response.data);
        }).catch((error) => {
            console.error('Error in login request:', error);
        });
    },
    pullComments(context, payload) {
        let authCookie = null;
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${'authToken'}=`);
        if (parts.length === 2) {
            authCookie = parts.pop().split(';').shift();
            const data = {
                authToken: authCookie,
                platform: payload.platform,
                movie: payload.movie
            };
            console.log("@pullComments");
            axios({
                url: localURL + "comments/pullcomments",
                method: "POST",
                data: data,
                withCredentials: true,
                headers: {
                    'X-CSRFToken': context.state.csrfToken,
                    'Content-Type': 'application/json', // Add this line
                }
            }).then((response) => {
                console.log("Comments pulled");
            }).catch((error) => {
                console.error('Error in login request:', error);
            });
        } else {
            alert("You are not logged in");
        }
    },

    requestMovieNames(context) {
        return new Promise((resolve, reject) => {
            let authCookie = null;
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${'authToken'}=`);

            if (parts.length === 2) {
                authCookie = parts.pop().split(';').shift();
                const data = {
                    authToken: authCookie
                };
                console.log("@requestMovieNames");
                axios({
                    url: localURL + "comments/getmovienames",
                    method: "POST",
                    data: data,
                    withCredentials: true,
                    headers: {
                        'X-CSRFToken': context.state.csrfToken,
                        'Content-Type': 'application/json',
                    }
                }).then((response) => {
                    context.commit('setMovieNames', response.data);
                    resolve(response.data); // Resolve the promise with the data
                }).catch((error) => {
                    console.error('Error in login request:', error);
                    reject(error); // Reject the promise with the error
                });
            } else {
                alert("You are not logged in");
                reject("Not logged in"); // Reject the promise with a reason
            }
        });
    },
    testDb(context) {
        return new Promise((resolve, reject) => {
            let authCookie = null;
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${'authToken'}=`);

            if (parts.length === 2) {
                authCookie = parts.pop().split(';').shift();
                const data = {
                    authToken: authCookie
                };

                axios({
                    url: localURL + "mod/testdb",
                    method: "POST",
                    data: data,
                    withCredentials: true,
                    headers: {
                        'X-CSRFToken': context.state.csrfToken,
                        'Content-Type': 'application/json',
                    }
                }).then((response) => {
                    console.log(response.data)
                    resolve(response.data); // Resolve the promise with the data
                }).catch((error) => {
                    console.error('Error in login request:', error);
                    reject(error); // Reject the promise with the error
                });
            } else {
                alert("You are not logged in");
                reject("Not logged in"); // Reject the promise with a reason
            }
        });
    },


    testPopularDb(context) { 
        let authCookie = null;
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${'authToken'}=`);
        if (parts.length === 2) {
            authCookie = parts.pop().split(';').shift();
            const data = {
                authToken: authCookie
            };
            axios({
                url: localURL + "mod/testpopulardb",
                method: "POST",
                data: data,
                withCredentials: true,
                headers: {
                    'X-CSRFToken': context.state.csrfToken,
                    'Content-Type': 'application/json', // Add this line
                }
            }).then((response) => {
                console.log(response.data);
            }).catch((error) => {
                console.error('Error in login request:', error);
            });
        } else {
            alert("You are not logged in");
        }
    },
    checkEmptyComments(context) { 
        let authCookie = null;
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${'authToken'}=`);
        if (parts.length === 2) {
            authCookie = parts.pop().split(';').shift();
            const data = {
                authToken: authCookie
            };
            axios({
                url: localURL + "mod/checkemptycomments",
                method: "POST",
                data: data,
                withCredentials: true,
                headers: {
                    'X-CSRFToken': context.state.csrfToken,
                    'Content-Type': 'application/json', // Add this line
                }
            }).then((response) => {
                context.commit('setEmptyList', response.data);

            }).catch((error) => {
                console.error('Error in login request:', error);
            });
        } else {
            alert("You are not logged in");
        }
    },
    
    emptyYoutubeComments(context) { 
        let authCookie = null;
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${'authToken'}=`);
        if (parts.length === 2) {
            authCookie = parts.pop().split(';').shift();
            const data = {
                authToken: authCookie
            };
            axios({
                url: localURL + "mod/emptyyoutubecomments",
                method: "POST",
                data: data,
                withCredentials: true,
                headers: {
                    'X-CSRFToken': context.state.csrfToken,
                    'Content-Type': 'application/json', // Add this line
                }
            }).then((response) => {
                console.log(response);
            }).catch((error) => {
                console.error('Error in login request:', error);
            });
        } else {
            alert("You are not logged in");
        }
    },
    analyseSentiment(context, payload) {
            let authCookie = null;
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${'authToken'}=`);
            if (parts.length === 2) {
                authCookie = parts.pop().split(';').shift();
                const data = {
                    authToken: authCookie,
                    is_reddit: payload.is_reddit,
                    is_youtube: payload.is_youtube,
                    movieNames: payload.movieNames
                };
                axios({
                    url: localURL + "comments/analysesentiment",
                    method: "POST",
                    data: data,
                    withCredentials: true,
                    headers: {
                        'X-CSRFToken': context.state.csrfToken,
                        'Content-Type': 'application/json',
                    }
                }).then((response) => {
                    console.log(response.data);
                }).catch((error) => {
                    console.error('Error in login request:', error);
                });
            } else {
                alert("You are not logged in");
            }
        
    }


};
