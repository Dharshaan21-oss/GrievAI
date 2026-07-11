import { createContext, useContext, useState, useEffect } from 'react'
import { loginUser, getCurrentUser } from '../api/auth'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('grievai_token')
    if (token) {
      getCurrentUser()
        .then((res) => setUser(res.data))
        .catch(() => {
          localStorage.removeItem('grievai_token')
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const login = async (email, password) => {
    const data = await loginUser(email, password)
    localStorage.setItem('grievai_token', data.access_token)
    const res = await getCurrentUser()
    setUser(res.data)
    return res.data
  }

  const logout = () => {
    localStorage.removeItem('grievai_token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}