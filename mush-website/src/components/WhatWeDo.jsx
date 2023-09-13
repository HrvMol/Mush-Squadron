import React from 'react'

export const WhatWeDo = () => (
    <section className='flex flex-col items-center px-[120px] pt-[130px] gap-10'>
        <div className='h-2.5 self-stretch rounded-full dark:bg-custom-white bg-custom-black' />
        <div className='flex md:flex-row flex-col gap-10 self-stretch'>
            <h1 className='font-karla text-[64px] dark:text-custom-white text-custom-black uppercase md:w-[40vw]'>What We Do?</h1>
            <p className='font-karla text-[36px] dark:text-custom-white text-custom-black uppercase'>We play Squadron Realistic Battles and compete for the top spot.</p>
        </div>

        <div className='h-2.5 mt-10 self-stretch rounded-full dark:bg-custom-white bg-custom-black' />
        <div className='flex md:flex-row flex-col gap-10 self-stretch'>
            <h1 className='font-karla text-[64px] dark:text-custom-white text-custom-black uppercase md:w-[40vw]'>What Is SRB?</h1>
            <p className='font-karla text-[36px] dark:text-custom-white text-custom-black uppercase'>
                SRB IS AN 8v8 VERSION OF GROUND RB WITH THE FOLLOWING CHANGES:
                <br /><br />
                - YOU ONLY GET 1 SPAWN, NO RE-SPAWNING.<br />
                - EACH TEAM CAN SPAWN 4 AIRCRAFT MAX.<br />
                - ONLY BOMBERS GET AIR SPAWNS.<br />
                - LIMITED DETECTION RANGE FOR AIRCRAFT.<br />
            </p>
        </div>

        <div className='h-2.5 mt-10 self-stretch rounded-full dark:bg-custom-white bg-custom-black' />
        <div className='flex md:flex-row flex-col gap-10 self-stretch'>
            <h1 className='font-karla text-[64px] dark:text-custom-white text-custom-black uppercase md:w-[40vw]'>What You Need</h1>
            <p className='font-karla text-[36px] dark:text-custom-white text-custom-black uppercase'>At least one ground vehicle from the tech tree at BR 9.7 or higher</p>
        </div>
    </section>
)
