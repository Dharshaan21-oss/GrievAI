import apiClient from './client'

export const registerUser = (data) => {
  return apiClient.post('/api/auth/register', data)
}

export const loginUser = async (email, password) => {
  // FastAPI's OAuth2PasswordRequestForm expects form-urlencoded data,
  // not JSON, with the field named "username" even though it's an email
  const params = new URLSearchParams()
  params.append('username', email)
  params.append('password', password)

  const response = await apiClient.post('/api/auth/login', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return response.data
}

export const getCurrentUser = () => {
  return apiClient.get('/api/auth/me')
}