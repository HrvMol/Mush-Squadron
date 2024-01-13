const express = require('express')
const cors = require('cors')

const db = require('./database')

const app = express()

// fixes issue with cors running on localhost
app.use(cors())

app.get('/users', db.getUsers)
app.get('/settings/:setting', db.getSetting)

app.listen(5000, () => console.log("Server on port 5000"))