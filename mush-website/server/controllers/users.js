import pkg from 'pg';
const { Pool } = pkg;

// connect to database
const pool = new Pool({
    // host: '192.168.0.231',
    host: 'localhost',
    port: 5432,
    database: 'postgres',
    user: 'postgres',
    password: 'postgres'
})

const getUsers = (req, res) => {
    pool.query('SELECT * FROM webscraper', (error, results) => {
      if (error) {
        throw error
      }
    //   not neccessary to give the 200 code but is good practice
      res.status(200).json({"users": results.rows})
    })
}

const getUser = (req, res) => {
    const id = BigInt(req.params.id)
    pool.query('SELECT * FROM webscraper WHERE discord_id = $1', [id], (error, results) => {
        if (error) {
            throw error
        }
        res.status(200).json(results.rows)
    })
}

const addUser = (req, res) => {
    const user = req.body
    console.log(user.query)
    pool.query(user.query, (error, results) => {
        if (error) {
            throw error
        }
        res.status(200).send("query complete")
    })
}

export { getUsers, getUser, addUser }