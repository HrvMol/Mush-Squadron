import React, { useEffect, useState} from 'react'

var prevCol = ''

// table to be displayed of the data for the members in the squadron
export default function Table() {
    // useState used to tell the element to update
    const [data, setData] = useState([{}])

    // sends request for the data and then sets it once recieved
    useEffect (() => {
        fetch("http://localhost:5000/users").then(
            response => response.json()
        ).then(
            data => {
                setData(data)
                console.log(data.users)
            }
        )
    }, [])

    function sortCols(col) {
        // needed to update table content in realtime without needing to refresh page
        // seperates each user out into it own so it can be iteratively manipulated
        const updateData = [...data.users]

        console.log(updateData[0][col])

        // checking if it is a number and applying the number sort
        if (updateData[0][col] === parseInt(data.users[0][col], 10)) {
            // checks if it should sort ascending or descending
            if (prevCol == col) {
                // contents of the sort function is used to sort the numbers
                // setData(updateData.sort((a,b) => b[col]-a[col]).reverse())
                setData({"users": updateData.sort((a,b) => b[col]-a[col]).reverse()})
                
                // resetting the order for ascending/descending
                prevCol = ''
            } else {
                // placing the data back into the users object for use in the mapping operation performed to display the items in the table
                setData({"users": updateData.sort((a,b) => b[col]-a[col])})

                prevCol = col
            }
        }
    }

    return (
        <div>
            {/* checking if data hasnt been retrieved yet then displaying loading if so */}
            {(typeof data.users === 'undefined') ? (
                <p>Loading...</p>
            ): (
                <table className='w-[80vw] dark:text-custom-white text-custom-black text-center'>
                    {/* header element */}
                    <thead>
                        <tr>
                            <td className='border-2 dark:border-custom-grey border-custom-black bg-custom-red py-0.5' />
                            <th className='border-2 dark:border-custom-grey border-custom-black bg-custom-red cursor-pointer' onClick={() => sortCols('player')}>Username</th>
                            <th className='border-2 dark:border-custom-grey border-custom-black bg-custom-red cursor-pointer' onClick={() => sortCols('clan_rating')}>SRB Points</th>
                            <th className='border-2 dark:border-custom-grey border-custom-black bg-custom-red cursor-pointer' onClick={() => sortCols('activity')}>Activity</th>
                            <th className='border-2 dark:border-custom-grey border-custom-black bg-custom-red cursor-pointer' onClick={() => sortCols('entry_date')}>Messages Sent</th>
                            <th className='border-2 dark:border-custom-grey border-custom-black bg-custom-red cursor-pointer' onClick={() => sortCols('messages_sent')}>VC Time</th>
                            <th className='border-2 dark:border-custom-grey border-custom-black bg-custom-red cursor-pointer' onClick={() => sortCols('vc_time')}>Join Date</th>
                        </tr>
                    </thead>
                    {/* mapping the data to create a row for each member and inputting their data */}
                    {data.users.map((val, key) => {
                        return (
                            <tbody key={key}>
                                <tr>
                                    <td className='border-2 dark:border-custom-grey border-custom-black py-0.5'>{key + 1}</td>
                                    <td className='border-2 dark:border-custom-grey border-custom-black'>{val.player}</td>
                                    <td className='border-2 dark:border-custom-grey border-custom-black'>{val.clan_rating}</td>
                                    <td className='border-2 dark:border-custom-grey border-custom-black'>{val.activity}</td>
                                    <td className='border-2 dark:border-custom-grey border-custom-black'>{val.messages_sent}</td>
                                    <td className='border-2 dark:border-custom-grey border-custom-black'>{val.vc_time}</td>
                                    {/* removing unnecessary info and reformatting from yyyy-mm-dd to dd/mm/yyyy */}
                                    <td className='border-2 dark:border-custom-grey border-custom-black'>{val.entry_date.slice(0, 10).split('-').reverse().join('/')}</td>
                                </tr>
                            </tbody>
                        )
                    })}
                </table>
            )}
        </div>

    )
}

// // table to be displayed of the data for the members in the squadron
// const Table = () => {
//     const [data, setData] = useState([{}])

//     useEffect (() => {
//         fetch("http://localhost:5000/users").then(
//             response => response.json()
//         ).then(
//             data => {
//                 setData(data)
//             }
//         )
//     }, [])

//     return (
//         <div>
//             {/* checking if data hasnt been retrieved yet then displaying loading if so */}
//             {(typeof data.users === 'undefined') ? (
//                 <p>Loading...</p>
//             ): (
//                 <table className='w-[80vw]'>
//                     {/* header element */}
//                     <thead>
//                         <tr>
//                             <td className='border-2 border-custom-black bg-custom-red' />
//                             <th className='border-2 border-custom-black bg-custom-red' onClick={() => sortCols('username')}>Username</th>
//                             <th className='border-2 border-custom-black bg-custom-red' onClick={() => sortCols('points')}>SRB Points</th>
//                             <th className='border-2 border-custom-black bg-custom-red' onClick={() => sortCols('activity')}>Activity</th>
//                             <th className='border-2 border-custom-black bg-custom-red' onClick={() => sortCols('joindate')}>Join Date</th>
//                         </tr>
//                     </thead>
//                     {/* mapping the data to create a row for each member and inputting their data */}
//                     {data.users.map((val, key) => {
//                         return (
//                             <tbody key={key}>
//                                 <tr>
//                                     <td className='border-2 border-custom-black'>{key + 1}</td>
//                                     <td className='border-2 border-custom-black'>{val.player}</td>
//                                     <td className='border-2 border-custom-black'>{val.clan_rating}</td>
//                                     <td className='border-2 border-custom-black'>{val.activity}</td>
//                                     {/* removing unnecessary info and reformatting from yyyy-mm-dd to dd/mm/yyyy */}
//                                     <td className='border-2 border-custom-black'>{val.entry_date.slice(0, 10).split('-').reverse().join('/')}</td>
//                                 </tr>
//                             </tbody>
//                         )
//                     })}
//                 </table>
//             )}
//         </div>

//     )
// }