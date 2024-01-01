import React from 'react'

// data to be put into the table
const data = [
    { username: "Header1234", points: 896, activity: "3045", joindate: "18/4/2022" },
    { username: "wall763abrasive", points: 542, activity: "381", joindate: "6/5/2021" },
    { username: "MrTacoDoesGames", points: 258, activity: "270", joindate: "20/5/2022" },
]
// table to be displayed of the data for the members in the squadron
const Table = () => {
  return (
    <table>
        {/* header element */}
        <tr>
            <th>Username</th>
            <th>SRB Points</th>
            <th>Activity</th>
            <th>Join Date</th>
        </tr>
        {/* mapping the data to create a row for each member and inputting their data */}
        {data.map((val, key) => {
            return (
                <tr key={key}>
                    <td>{val.username}</td>
                    <td>{val.points}</td>
                    <td>{val.activity}</td>
                    <td>{val.joindate}</td>
                </tr>
            )
        })}
    </table>
  )
}

export default Table