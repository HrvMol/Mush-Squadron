import React, { useEffect, useState} from 'react'

var prevCol = ''

// table to be displayed of the data for the members in the squadron
export default function Table() {
    // useState used to tell the element to update
    const [data, setData] = useState([{}])

    // sends request for the data and then sets it once recieved
    useEffect (() => {
        fetch("http://localhost:5000/api/users").then(
            response => response.json()
        ).then(
            data => {
                setData(data)
            }
        )
    }, [])

    function sortCols(col) {
        // needed to update table content in realtime without needing to refresh page
        // seperates each user out into its own so it can be iteratively manipulated
        const updateData = [...data.users]

        console.log(col)

        // checking if it is a number and applying the number sort
        if (updateData[0][col] === parseInt(data.users[0][col], 10)) {
            // checks if it should sort ascending or descending
            if (prevCol == col) {
                // contents of the sort function is used to sort the numbers
                setData({"users": updateData.sort((a,b) => a[col]-b[col])})
                
                // resetting the order for ascending/descending
                prevCol = ''
            } else {
                // placing the data back into the users object for use in the mapping operation performed to display the items in the table
                setData({"users": updateData.sort((a,b) => b[col]-a[col])})

                prevCol = col
            }
        } else if (col == 'player') {
            if (prevCol == col) {
                // contents of the sort function is used to sort the names
                setData({"users": updateData.sort((a, b) => {
                    // converts to lowercase to avoid issues when comparing uppercase to lowercase
                    let na = a.player.toLowerCase()
                    let nb = b.player.toLowerCase()

                    // comparing which value is greater then telling the sort which to move or to not move at all
                    if (na < nb) {
                        return 1
                    } else if (na > nb) {
                        return -1
                    } else return 0
                })})
                
                // resetting the order for ascending/descending
                prevCol = ''
            } else {
                // contents of the sort function is used to sort the names
                setData({"users": updateData.sort((a, b) => {
                    // converts to lowercase to avoid issues when comparing uppercase to lowercase
                    let player1 = a.player.toLowerCase()
                    let player2 = b.player.toLowerCase()

                    // comparing which value is greater then telling the sort which to move or to not move at all
                    if (player1 < player2) {
                        return -1
                    } else if (player1 > player2) {
                        return 1
                    } else return 0
                })})

                prevCol = col
            }
        } else if (col == 'entry_date') {
            // checks if it should sort ascending or descending
            if (prevCol == col) {
                // contents of the sort function is used to sort the numbers
                setData({"users": updateData.sort((a,b) => {
                    // removes useless data and then creates date object
                    let date1 = new Date(a.entry_date.slice(0, 10))
                    let date2 = new Date(b.entry_date.slice(0, 10))

                    return date2 - date1
                })})
                
                // resetting the order for ascending/descending
                prevCol = ''
            } else {
                // placing the data back into the users object for use in the mapping operation performed to display the items in the table
                setData({"users": updateData.sort((a,b) => {
                    // removes useless data and then creates date object
                    let date1 = new Date(a.entry_date.slice(0, 10))
                    let date2 = new Date(b.entry_date.slice(0, 10))

                    return date1 - date2
                })})

                prevCol = col
            }
        }
    }

    return (
        <div>
            {/* checking if data hasnt been retrieved yet then displaying loading if so */}
            {(typeof data.users === 'undefined') ? (
                <p className='font-karla lg:text-[96px] text-[70px] font-[500] dark:text-custom-white text-custom-black text-center'>Loading...</p>
            ): (
                <table className='w-[80vw] dark:text-custom-white text-custom-black text-center'>
                    {/* header element */}
                    <thead>
                        <tr>
                            <td className='border-2 dark:border-custom-grey border-custom-black bg-custom-red py-0.5' />
                            <th className='border-2 dark:border-custom-grey border-custom-black bg-custom-red cursor-pointer' onClick={() => sortCols('player')}>Username</th>
                            <th className='border-2 dark:border-custom-grey border-custom-black bg-custom-red cursor-pointer' onClick={() => sortCols('clan_rating')}>SRB Points</th>
                            <th className='border-2 dark:border-custom-grey border-custom-black bg-custom-red cursor-pointer' onClick={() => sortCols('activity')}>Activity</th>
                            <th className='border-2 dark:border-custom-grey border-custom-black bg-custom-red cursor-pointer' onClick={() => sortCols('messages_sent')}>Messages Sent</th>
                            <th className='border-2 dark:border-custom-grey border-custom-black bg-custom-red cursor-pointer' onClick={() => sortCols('vc_time')}>Minutes in VC</th>
                            <th className='border-2 dark:border-custom-grey border-custom-black bg-custom-red cursor-pointer' onClick={() => sortCols('entry_date')}>Join Date</th>
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