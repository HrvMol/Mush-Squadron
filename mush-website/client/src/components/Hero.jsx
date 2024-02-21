import React from 'react'

export const Hero = () => (
    <section className='w-full flex md:flex-row flex-col px-[120px] justify-between items-center gap-[120px]'>
        <div className='flex flex-col items-start gap-[90px] max-w-[800px] md:w-[40vw] w-[90vw]'>
            <h1 className='font-karla lg:text-[96px] text-[70px] font-[500] md:text-left text-center self-center dark:text-custom-white text-custom-black uppercase'>Mush <br /> War Thunder</h1>
            <div className='flex flex-col p-[10px] items-start gap-[30px] self-stretch'>
                <p className='font-karla text-[36px] font-[500] md:text-left text-center dark:text-custom-white text-custom-black uppercase'>
                    Mush is a top 100 competetive War Thunder squadron. <br /><br />
                    We are the result of years of hard work.
                </p>
                <a href='https://discord.gg/u2v98rdBcJ' className='px-4 py-2 rounded-full bg-custom-red md:self-start self-center'>
                    <p className='font-karla font-normal text-[24px] text-center dark:text-custom-white text-custom-black uppercase '>Join The Squadron Now</p>
                </a>
            </div>
        </div>
        <div className='p-[120px] dark:bg-gradient-radial-dark bg-gradient-radial-light'>
            <img src='src\assets\Artboard 1.png' className='min-w-[77px]'/>
        </div>
    </section>
)
