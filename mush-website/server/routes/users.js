import express from 'express'
import { getUsers, getUser, addUser } from '../controllers/users.js'
import auth from '../middleware/auth.js'

const router = express.Router()

router.get('/users', getUsers)
router.get('/users/:id', getUser)
router.post('/users', [auth], addUser)

export default router