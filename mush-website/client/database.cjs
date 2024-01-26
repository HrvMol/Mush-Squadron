const {Client} = require('pg')

const client = new Client({
    host: 'localhost',
    port: 5432,
    database: 'postgres',
    user: 'postgres',
    password: 'postgres'
})

client.connect()

client.query(`Select * from webscraper`, (err, res)=>{
    if (!err){
        console.log(res)
    } else {
        console.log(err.message)
    }
    client.end
})