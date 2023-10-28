/* eslint-disable no-unused-vars */
import axios from 'axios';
export default {

    async getMovieData(context) {
        const payload = await axios({
            url: "https://ym-project.vercel.app",
            method: "GET"
        })
        context.commit('setMovieData', payload.data)
    }
}