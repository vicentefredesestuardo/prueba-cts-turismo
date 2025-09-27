export default defineNuxtRouteMiddleware(() => {
  if (!process.client) return

  const token = localStorage.getItem('access_token')
  if (!token) {
    return navigateTo('/admin/login')
  }

  // (Opcional) Validar expiración del JWT sin pegarle al backend
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    const now = Math.floor(Date.now() / 1000)
    if (payload.exp && payload.exp <= now) {
      localStorage.removeItem('access_token')
      return navigateTo('/admin/login')
    }
  } catch {
    // Si el token está corrupto, limpia y redirige
    localStorage.removeItem('access_token')
    return navigateTo('/admin/login')
  }
})
