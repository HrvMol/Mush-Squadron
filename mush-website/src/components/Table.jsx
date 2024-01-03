import { useState } from "react"
import React from 'react'

// var [data, setData] = useState([]);

// data to be put into the table
const initialData = [
    { username: "Header1234", points: 896, activity: 3045, joindate: "18/4/2022" },
    { username: "wall763abrasive", points: 542, activity: 270, joindate: "6/5/2021" },
    { username: "MrTacoDoesGames", points: 258, activity: 381, joindate: "20/5/2022" },
]

var prevCol = ''

// table to be displayed of the data for the members in the squadron
export default function Table() {
    // useState used to tell the element to update
    const [data, setData] = useState(initialData)

    function sortCols(col) {
        // needed to update table content in realtime without needing to refresh page
        const updateData = [...data]

        // checking if it is a number and applying the number sort
        if (updateData[0][col] === parseInt(data[0][col], 10)) {
            // checks if it should sort ascending or descending
            if (prevCol == col) {
                // contents of the sort function is used to sort the numbers
                setData(updateData.sort((a,b) => b[col]-a[col]).reverse())
    
                // resetting the order for ascending/descending
                prevCol = ''
            } else {
                setData(updateData.sort((a,b) => b[col]-a[col]))

                prevCol = col
            }
        }
    }

    return (
        <table className='w-[80vw]'>
            {/* header element */}
            <thead>
                <tr>
                    <td className='border-2 border-custom-black bg-custom-red'></td>
                    <td className='border-2 border-custom-black bg-custom-red' onClick={() => sortCols('username')}>Username</td>
                    <td className='border-2 border-custom-black bg-custom-red' onClick={() => sortCols('points')}>SRB Points</td>
                    <td className='border-2 border-custom-black bg-custom-red' onClick={() => sortCols('activity')}>Activity</td>
                    <td className='border-2 border-custom-black bg-custom-red' onClick={() => sortCols('joindate')}>Join Date</td>
                </tr>
            </thead>
            {/* mapping the data to create a row for each member and inputting their data */}
            {data.map((val, key) => {
                return (
                    <tbody key={key}>
                        <tr>
                            <td className='border-2 border-custom-black'>{key + 1}</td>
                            <td className='border-2 border-custom-black'>{val.username}</td>
                            <td className='border-2 border-custom-black'>{val.points}</td>
                            <td className='border-2 border-custom-black'>{val.activity}</td>
                            <td className='border-2 border-custom-black'>{val.joindate}</td>
                        </tr>
                    </tbody>
                )
            })}
        </table>
    )
}