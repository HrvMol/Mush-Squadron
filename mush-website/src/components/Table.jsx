import React, { useEffect, useState} from 'react'

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
}

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
                <table className='w-[80vw]'>
                    {/* header element */}
                    <thead>
                        <tr>
                            <td className='border-2 border-custom-black bg-custom-red' />
                            <th className='border-2 border-custom-black bg-custom-red' onClick={() => sortCols('username')}>Username</th>
                            <th className='border-2 border-custom-black bg-custom-red' onClick={() => sortCols('points')}>SRB Points</th>
                            <th className='border-2 border-custom-black bg-custom-red' onClick={() => sortCols('activity')}>Activity</th>
                            <th className='border-2 border-custom-black bg-custom-red' onClick={() => sortCols('joindate')}>Join Date</th>
                        </tr>
                    </thead>
                    {/* mapping the data to create a row for each member and inputting their data */}
                    {data.users.map((val, key) => {
                        return (
                            <tbody key={key}>
                                <tr>
                                    <td className='border-2 border-custom-black'>{key + 1}</td>
                                    <td className='border-2 border-custom-black'>{val.player}</td>
                                    <td className='border-2 border-custom-black'>{val.clan_rating}</td>
                                    <td className='border-2 border-custom-black'>{val.activity}</td>
                                    {/* removing unnecessary info and reformatting from yyyy-mm-dd to dd/mm/yyyy */}
                                    <td className='border-2 border-custom-black'>{val.entry_date.slice(0, 10).split('-').reverse().join('/')}</td>
                                </tr>
                            </tbody>
                        )
                    })}
                </table>
            )}
        </div>

    )
}