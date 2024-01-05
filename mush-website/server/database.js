const { Pool } = require("pg")

// connect to database
const pool = new Pool({
    host: 'localhost',
    port: 5432,
    database: 'postgres',
    user: 'postgres',
    password: 'postgres'
})

// get all users in table
const getUsers = (request, response) => {
  pool.query('SELECT * FROM webscraper', (error, results) => {
    if (error) {
      throw error
    }
  //   not neccessary to give the 200 code but is good practice
    response.status(200).json({"users": results.rows})
  })
}

module.exports = {
    getUsers
}