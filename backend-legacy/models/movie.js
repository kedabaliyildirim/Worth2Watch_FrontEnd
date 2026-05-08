const mongoose = require("mongoose");

const movieSchema = new mongoose.Schema({
  movieTitle: {
    type: String,
    required: true,
  },
  filmCover: {
    type: String,
    required: true,
  },
  releaseDate: {
    type: Date,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  genre: {
    type: String,
    required: true,
  },
 
});

module.exports = mongoose.model("Movie", movieSchema);
