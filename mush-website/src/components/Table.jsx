import React from 'react'

// data to be put into the table
const data = [
    { username: "Header1234", points: 896, activity: "3045", joindate: "18/4/2022" },
    { username: "wall763abrasive", points: 542, activity: "381", joindate: "6/5/2021" },
    { username: "MrTacoDoesGames", points: 258, activity: "270", joindate: "20/5/2022" },
]

var prevCol = ''
const sortCols = (col) => {
    var orderAsc = true
    if (prevCol = col) {
        orderAsc = false
        console.log(col + ' descending');
    }
    prevCol = col

    console.log(col + ' ascending');
   };

// table to be displayed of the data for the members in the squadron
const Table = () => {
  return (
    <table className='w-[80vw]'>
        {/* header element */}
        <thead>
            <td className='border-2 border-custom-black bg-custom-red' onClick={() => sortCols('username')}>Username</td>
            <td className='border-2 border-custom-black bg-custom-red' onClick={() => sortCols('points')}>SRB Points</td>
            <td className='border-2 border-custom-black bg-custom-red' onClick={() => sortCols('activity')}>Activity</td>
            <td className='border-2 border-custom-black bg-custom-red' onClick={() => sortCols('joindate')}>Join Date</td>
        </thead>
        {/* mapping the data to create a row for each member and inputting their data */}
        {data.map((val, key) => {
            return (
                <tbody key={key}>
                    <td className='border-2 border-custom-black'>{val.username}</td>
                    <td className='border-2 border-custom-black'>{val.points}</td>
                    <td className='border-2 border-custom-black'>{val.activity}</td>
                    <td className='border-2 border-custom-black'>{val.joindate}</td>
                </tbody>
            )
        })}
    </table>
  )
}

export default Table