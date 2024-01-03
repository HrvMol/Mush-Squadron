import React, { useEffect, useState} from 'react'

// data to be put into the table
const data = [
    { username: "Header1234", points: 896, activity: 3045, joindate: "18/4/2022" },
    { username: "wall763abrasive", points: 542, activity: 270, joindate: "6/5/2021" },
    { username: "MrTacoDoesGames", points: 258, activity: 381, joindate: "20/5/2022" },
]

var prevCol = ''
const sortCols = (col) => {
    if (data[0][col] === parseInt(data[0][col], 10)) {
        console.log('number')
    }
    if (prevCol == col) {
        console.log(data.sort((a,b) => b[col]-a[col]).reverse())
        console.log(col + ' descending')
        prevCol = ''
    } else {
        console.log(data.sort((a,b) => b[col]-a[col]))

        console.log(col + ' ascending')
        prevCol = col
    }
   };

// table to be displayed of the data for the members in the squadron
const Table = () => {
    const [data, setData] = useState([{}])

    useEffect (() => {
        fetch("http://localhost:5000/users").then(
            response => response.json()
        ).then(
            data => {
                setData(data)
            }
        )
    }, [])

    return (
        <div>
            {/* checking if data hasnt been retrieved yet then displaying loading if so */}
            {(typeof data.users === 'undefined') ? (
                <p>Loading...</p>
            ): (
                <table>
                    {/* header element */}
                    <tr>
                        <th>Username</th>
                        <th>SRB Points</th>
                        <th>Activity</th>
                        <th>Join Date</th>
                    </tr>
                    {/* mapping the data to create a row for each member and inputting their data */}
                    {data.users.map((val, key) => {
                        return (
                            <tr key={key}>
                                <td>{val.player}</td>
                                <td>{val.clan_rating}</td>
                                <td>{val.activity}</td>
                                {/* removing unnecessary info and reformatting from yyyy-mm-dd to dd/mm/yyyy */}
                                <td>{val.entry_date.slice(0, 10).split('-').reverse().join('/')}</td>
                            </tr>
                        )
                    })}
                </table>
            )}
        </div>

    )
}

export default Table