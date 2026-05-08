const express = require("express");
const dotenv = require("dotenv");

const db = require("./config/db.js");
const appConfig = require("./config/appConfig.js");

const Auth = require("./routes/auth.js");
const Movie = require("./routes/movie.js");
const User = require("./routes/user.js");

dotenv.config();
const app = express();

appConfig(app);

db();

// app.get("/", (req, res) => {
//     res.send("Hello World");
//     });

app.use('/auth', Auth);
app.use('/movie', Movie);
app.use('/settings', User);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${process.env.PORT}`);
});
