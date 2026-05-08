const User = require('../models/user.js');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const register = async (req, res) => {
    try {
        const {name, surname, email, password,profilePicture,role, birthDate, gender} = req.body;

        // Check if user with email already exists
        const existingUser = await User.findOne({ email });
        if (existingUser) {
            return res.status(400).json({ message: 'User already exists' });
        }

        // Check password length
        if (password.length < 6) {
            return res.status(400).json({ message: 'Password must be at least 6 characters' });
        }

        // Hash the password
        const passwordHash = await bcrypt.hash(password, 12);

        // Create new user
        const newUser = await User.create({ name, surname, email, password: passwordHash, profilePicture, role, birthDate, gender });

        // Generate JWT token. The original code referenced `user._id` and
        // returned an undefined `userToken` — both were typos that would
        // crash the route at runtime; fixed to use the freshly-created user.
        const token = jwt.sign({ id: newUser._id, role: newUser.role }, process.env.SECRET_TOKEN, { expiresIn: '1h' });
        res.status(201).json({
            status: 'OK',
            user: newUser,
            token,
        });

    } catch (error) {
        return res.status(500).json({ message: error.message });
    }
};

const login = async (req, res) => {
    try {
        const { email, password } = req.body;

        // Find user by email
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(404).json({ message: 'User does not exist' });
        }

        // Compare passwords
        const comparePassword = await bcrypt.compare(password, user.password);
        if (!comparePassword) {
            return res.status(400).json({ message: 'Password is incorrect' });
        }

        // Generate JWT token
        const token = jwt.sign({ id: user._id, role: user.role }, process.env.SECRET_TOKEN, { expiresIn: '1h' });
        res.status(200).json({
            status: 'OK',
            user,
            token
        });
    } catch (error) {
        return res.status(500).json({ message: error.message });
    }
};

module.exports = { register, login };
