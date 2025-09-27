// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  ssr: false,

  // 🔧 Fuerza el enrutador por archivos
  pages: true,
  srcDir: '.',                 // asegura raíz como src
  dir: { pages: 'pages' },     // apunta explícitamente a /pages

  // Módulos
  modules: [
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss' 
  ],
  
  // Configuración runtime para variables de entorno
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api' 
    }
  }
})
