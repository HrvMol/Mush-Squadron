import { useState } from 'react'
import { menu, close } from '../assets'
import { Link } from 'react-router-dom'


function Navbar(props) {
  const [toggle, setToggle] = useState(false)
  return (
    <nav className='w-full flex flex-row py-2 px-10 justify-between items-center dark:bg-custom-black bg-custom-white fixed navbar'>
      <Link to='/home' className='font-karla font-normal text-[24px] dark:text-custom-white text-custom-black uppercase'>Mush</Link>

      {/* Desktop view */}
      <ul className='list-none sm:flex hidden justify-end flex-1 items-center'>
        {/* <li>
          <Link to="/home" className='font-karla font-normal text-[24px] dark:text-custom-white text-custom-black uppercase leading-none'>Home</Link>
        </li>
        <li>
          <Link to="/gallery" className='font-karla font-normal text-[24px] dark:text-custom-white text-custom-black uppercase leading-none'>Gallery</Link>
        </li>
        <li>
          <Link to="/database" className='font-karla font-normal text-[24px] dark:text-custom-white text-custom-black uppercase leading-none'>Database</Link>
        </li>
        <li className=''>
          <a href='https://www.google.com/' className='px-3 pb-0.5 rounded-full bg-custom-red font-karla font-normal text-[24px] dark:text-custom-white text-custom-black uppercase leading-none'>
            Join Us
          </a>
        </li> */}
        { props.children }
      </ul>

      {/* Mobile view */}
      <div className='sm:hidden flex flex-1 justify-end items-center'>
        <img 
          src={toggle ? close : menu}
          alt='menu'
          className='w-[28px] h-[28px] object-contain'
          onClick={() => setToggle((prev) => !prev)}
        />

        <div className={`${toggle ? 'flex' : 'hidden'} p-6 bg-button absolute top-20 right-0 mx-4 my-2 min-w-[140px] rounded-xl dark:bg-custom-dark-grey bg-custom-grey sidebar`}>
          <ul className='list-none flex flex-col justify-end items-center flex-1 gap-3'>
            { props.children }
          </ul>
        </div>
      </div>
    </nav>
  )
}

function NavItem({to, text}) {
  return (
    <li>
      <Link to={ to } className='font-karla font-normal text-[24px] dark:text-custom-white text-custom-black uppercase leading-none sm:mr-10 mt-10'>
        { text }
      </Link>
    </li>
  )
}

function NavLink({to, text}) {
  return (
    <li className=''>
      <a href={ to } className='px-3 pb-0.5 rounded-full bg-custom-red font-karla font-normal text-[24px] dark:text-custom-white text-custom-black uppercase leading-none'>
        { text }
      </a>
    </li>
  )
}

export { Navbar, NavItem, NavLink }