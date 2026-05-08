const mongoose = require("mongoose");


// Connect to MongoDB
const db =() => {
mongoose.connect(process.env.MONGO_URI, {
    
    }).then(() => {
        console.log("DB connected");
    }).catch((err) => {
        console.log("DB connection error: ", err);
    });
}

module.exports = db;


