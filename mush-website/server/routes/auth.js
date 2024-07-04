import jwt from 'jsonwebtoken';
import express from 'express';
import pool from '../database.js';
import auth from '../middleware/auth.js';

const router = express.Router();

router.post('/login', async (req, res) => {
    const { username, password } = req.body;

    const user = await pool.query('SELECT * FROM tokenauth WHERE username=$1', [username])

    if(password !== user.rows[0].password){
        return res.status(401).send({success: false, error: 'Invalid password'});
    }
    
    const token = jwt.sign({username}, process.env.JWT_SECRET, {expiresIn: '1h'});
    return res.status(200).send({success: true, token: token});
});

router.get('/verify', [auth], (req, res) => {
    return res.status(200).send({success: true});
});

export default router;