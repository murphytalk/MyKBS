/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/main/*.ts',
    './src/preload/*.ts',
    './src/renderer/*.html',
    './src/renderer/**/*.{js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {}
  },
  plugins: []
}
