/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}", "./src/components/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        'silkscreen': 'Silkscreen',
        'roboto': 'Roboto',
      },
      boxShadow: {
        'inner-dark': 'inset 0 4px 6px rgba(0, 0, 0, 0.1)',
        '2xl-dark': '0 25px 25px rgba(0, 0, 0, 0.15)',
      },
    },
  },
  plugins: [],
}

