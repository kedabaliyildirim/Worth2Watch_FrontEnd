const express = require("express");
const router = express.Router();
const { updateProfilePicture, updateEmail, updatePassword, deleteUserAccount } = require("../controllers/user.js");
const  auth  = require("../middleware/auth.js");

router.patch("/profilePicture", auth, updateProfilePicture);

router.patch("/email", auth, updateEmail);

router.patch("/password", auth, updatePassword);

router.delete("/account", auth, deleteUserAccount);

module.exports = router;
