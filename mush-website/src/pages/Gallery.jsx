import React from 'react'
import { Navbar, NavItem, NavLink } from '../components'

export const Gallery = () => (
  <div className="w-full overflow-hidden relative min-h-[100vh] bg-gradient-to-b dark:from-custom-black dark:to-custom-dark-grey from-custom-white to-custom-grey">
    <div className='flex justify-center items-center'>
        <div className='w-full'>
          <Navbar>
            <NavItem to='/' text='Home' />
            <NavItem to='/gallery' text='Gallery' />
            <NavItem to='/database' text='Database' />
            <NavLink to='https://discord.gg/JkJvjfkXzU' text='Join Us' />
          </Navbar>
        </div>
    </div>
  </div>
)
