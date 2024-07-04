import express from 'express'
import cors from 'cors'
import bodyParser from 'body-parser'

import dotenv from 'dotenv';
dotenv.config();

// const db = require('./database')
import userRoutes from './routes/users.js'
import authRoutes from './routes/auth.js'

const app = express()

// fixes issue with cors running on localhost
app.use(cors())
app.use(bodyParser.json())

app.use('/', userRoutes)
app.use('/auth', authRoutes)

app.get('/', (req, res) => {
    res.send("Hello World")
})

// app.get('/users', db.getUsers)
// NOT USED
// app.get('/settings/:setting', db.getSetting)

app.listen(5000, () => console.log("Server on port: http://localhost:5000"))