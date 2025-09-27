export const useApi = () => {
  const { public: { apiBase } } = useRuntimeConfig()

  const getToken = () => (process.client ? localStorage.getItem('access_token') : null)

  const apiFetch = (url: string, options: any = {}) => {
    const token = getToken()
    return $fetch(url, {
      baseURL: apiBase, 
      headers: {
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...(options.headers || {}),
      },
      ...options,
    })
  }

  // Público
  const registerContestant = (data: any) =>
    apiFetch('/contestants/', { method: 'POST', body: data })

  const verifyEmail = (data: any) =>
    apiFetch('/verification/', { method: 'POST', body: data })

  // Admin auth (SimpleJWT)
  const adminLogin = (data: any) =>
    apiFetch('/admin/login/', { method: 'POST', body: data })

  // Admin recursos
  const getContestants = (params: Record<string, any> = {}) => {
    const query = new URLSearchParams(params as any).toString()
    return apiFetch(`/admin/contestants/${query ? `?${query}` : ''}`)
  }

  const drawWinner = () =>
    apiFetch('/admin/winner/', { method: 'POST' })

  const getWinner = () =>
    apiFetch('/admin/winner/')

  return {
    apiFetch,
    registerContestant,
    verifyEmail,
    adminLogin,
    getContestants,
    drawWinner,
    getWinner,
  }
}
