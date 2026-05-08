const express = require("express");
const { getAllMovies, getMovieDetail, createMovie, updateMovie, deleteMovie } = require("../controllers/movie.js");
const isAdmin = require("../middleware/isAdmin.js");

const router = express.Router();

router.get("/", getAllMovies);
router.get("/:id", getMovieDetail);
router.post("/", isAdmin, createMovie);
router.patch("/:id", isAdmin, updateMovie);
router.delete("/:id", isAdmin, deleteMovie);

module.exports = router;
