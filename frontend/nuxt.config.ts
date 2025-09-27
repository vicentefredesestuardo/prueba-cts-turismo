// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  
  // Módulos
  modules: [
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss' // ← MANTENER para la prueba técnica
  ],
  
  // Configuración runtime para variables de entorno
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api' 
  }
})
