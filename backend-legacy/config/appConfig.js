const cors = require("cors");
const express = require("express");

const appConfig = (app) => {
    app.use(cors());
    app.use(express.json()); 
   
};

module.exports = appConfig;
