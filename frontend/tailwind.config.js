/** @type {import('tailwindcss').Config} */
export default {
  // Aquí le decimos a Tailwind que "mire"
  // todos nuestros archivos HTML y JSX en busca de clases.
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}