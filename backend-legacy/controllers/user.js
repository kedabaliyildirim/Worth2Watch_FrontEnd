const User = require('../models/user.js');
const bcrypt = require('bcryptjs');

const updateProfilePicture = async (req, res) => {
    try {
        const { profilePicture } = req.body;
        const userId = req.user.id; 

        console.log(req.user.id);
        console.log(userId);
       

        const user = await User.findByIdAndUpdate(userId, { profilePicture }, { new: true });
        res.status(200).json({ user });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
}

const updateEmail = async (req, res) => {
    try {
        const { email } = req.body;
        const userId = req.user.id; // Kullanıcının kimliğini al

         const user = await User.findByIdAndUpdate(userId, { email }, { new: true });
        res.status(200).json({ user });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
}

const updatePassword = async (req, res) => {
    try {
        const { password } = req.body;
        const userId = req.user.id; // Kullanıcının kimliğini al

        // Kullanıcının kendi şifresini güncellemesini sağlamak için doğrulama ekleyin
        if (req.userId !== userId) {
            return res.status(403).json({ message: 'Unauthorized: You are not authorized to perform this action' });
        }

        // Şifreyi hash'leyin ve güncelleyin
        const passwordHash = await bcrypt.hash(password, 12);
        const user = await User.findByIdAndUpdate(userId, { password: passwordHash }, { new: true });
        res.status(200).json({ user });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
}

const deleteUserAccount = async (req, res) => {
    try {
        const userId = req.user.id; // Kullanıcının kimliğini al

        // Kullanıcının kendi hesabını silmesini sağlamak için doğrulama ekleyin
        if (req.userId !== userId) {
            return res.status(403).json({ message: 'Unauthorized: You are not authorized to perform this action' });
        }

        // Hesabı sil
        await User.findByIdAndDelete(userId);
        res.status(200).json({ message: 'User account is deleted' });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
}

module.exports = { updateProfilePicture, updateEmail, updatePassword, deleteUserAccount };
