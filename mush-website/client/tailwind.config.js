/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    colors: {
      'custom-white': '#FAFAFA',
      'custom-grey': '#EAEAEA',
      'custom-dark-grey': '#2E2E2E',
      'custom-black': '#121212',
      'custom-red': '#F05D5E',
    },
    extend: {
      backgroundImage: {
        'gradient-radial-dark': 'radial-gradient(50.00% 50.00% at 50.00% 50.00%, #F05D5E 21.62%, rgba(28, 28, 28, 0.00) 100%)',
        'gradient-radial-light': 'radial-gradient(50.00% 50.00% at 50.00% 50.00%, #F05D5E 21.62%, rgba(255, 255, 255, 0.00) 100%)',
      },
    },
  },
  plugins: [],
}

