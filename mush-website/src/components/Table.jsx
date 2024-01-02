import React, { useEffect, useState} from 'react'

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