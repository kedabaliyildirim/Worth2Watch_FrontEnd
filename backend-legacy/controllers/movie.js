const movieSchema = require("../models/movie.js");

const createMovie = async (req, res) => {
  try {
    const newMovie = await movieSchema.create(req.body);

    res.status(201).json(newMovie);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};



const getMovieDetail = async (req, res) => {
    try {
        const{ id } = req.params; 
        const detailMovie = await movieSchema.findById(id);
        res.status(200).json({
            detailMovie
        });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
}

const updateMovie = async (req, res) => {
    try {
        const { id } = req.params;
        const updateMovie = await movieSchema.findByIdAndUpdate(id,req.body,{new:true});
        res.status(200).json({
            updateMovie
        });
    }
    catch (error) {
        res.status(500).json({ message: error.message });
    }
}

const deleteMovie = async (req, res) => {
    try {
        const { id } = req.params;
        await movieSchema.findByIdAndDelete(id);
        res.status(201).json({ message: 'Movie is deleted' });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
}


const getAllMovies = async (req, res) => {
  const { page = 1, sort = 'releaseDate', genre } = req.query;
  const limit = 6; // How many movies to show per page

  const query = genre ? { genre } : {};

  try {
    const movies = await movieSchema.find(query)
      .sort(sort)
      .limit(limit)
      .skip((page - 1) * limit)
      .exec();

    const count = await movieSchema.countDocuments(query);

    res.json({
      totalPages: Math.ceil(count / limit),
      currentPage: page,
      movies
    });
  } catch (err) {
    console.error(err);
    res.status(500).send(err);
  }
};

module.exports = {getAllMovies, createMovie, getMovieDetail, updateMovie, deleteMovie};
