const  mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
    },
    surname: {
        type: String,
        required: true,
    },
    email: {
        type: String,
        required: true,
    },
    password: {
        type: String,
        required: true,
    },
    profilePicture: {
        type: String,
        default: ""
    },
    role: {
        type: String,
        enum: ['admin', 'user'],
        default: 'user' 
      },
    birthDate: {
        type: Date,
        default: Date.now(),
    },
    gender: {
        type: String,
        default:""
    },

});


module.exports = mongoose.model("User", userSchema);

