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

export default pool