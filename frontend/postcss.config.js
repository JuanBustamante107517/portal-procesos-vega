// frontend/postcss.config.js
export default {
  plugins: {
    // ANTES decía: 'tailwindcss': {},
    // AHORA usamos el nuevo paquete:
    '@tailwindcss/postcss': {}, 
    'autoprefixer': {},
  },
}