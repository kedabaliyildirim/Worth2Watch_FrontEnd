const jwt = require('jsonwebtoken');

const isAdmin = (req, res, next) => {
    try {
        const token = req.headers.authorization.split(' ')[1];
        const decodedData = jwt.verify(token, process.env.SECRET_TOKEN);
        
        // Kullanıcının admin rolüne sahip olup olmadığını kontrol et
        if (decodedData.role !== 'admin') {
            return res.status(403).json({ message: 'Unauthorized: Only admin users can access this resource' });
        }
        
        req.userId = decodedData.id;
        next();
    } catch (error) {
        return res.status(401).json({ message: 'Unauthorized: Invalid or missing token' });
    }
};

module.exports = isAdmin;
