import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Attach the JWT token to every request automatically, if we have one
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('grievai_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// If the server ever returns 401 (expired/invalid token), auto-log the user out
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('grievai_token')
      localStorage.removeItem('grievai_user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default apiClient