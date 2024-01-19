import React from 'react'
import { Navbar, NavItem, NavLink, ComingSoon, Footer, Table } from '../components'

export const Database = () => (
  <div className="w-full overflow-hidden relative min-h-[100vh] bg-gradient-to-b dark:from-custom-black dark:to-custom-dark-grey from-custom-white to-custom-grey">
    <div className='flex justify-center items-center'>
        <div className='w-full'>
          <Navbar>
            <NavItem to='/' text='Home' />
            <NavItem to='/database' text='Database' />
            <NavLink to='https://discord.gg/JkJvjfkXzU' text='Join Us' />
          </Navbar>
        </div>
    </div>

    <div className='flex justify-center items-center pt-[160px]'>
      <div className='pb-36'>
        <Table />
        {/* <ComingSoon /> */}
      </div>
      <Footer />
    </div>
  </div>
)
