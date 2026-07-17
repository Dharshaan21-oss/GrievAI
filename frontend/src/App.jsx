import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import AdminDashboard from './pages/AdminDashboard'
import './App.css'
import NearbyFeed from './pages/NearbyFeed'

function ProtectedRoute({ children, requireStaff = false }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="p-8 text-center">Loading...</div>
  if (!user) return <Navigate to="/login" />
  if (requireStaff && !['official', 'admin'].includes(user.role)) {
    return <Navigate to="/dashboard" />
  }
  return children
}

function HomeRedirect() {
  const { user, loading } = useAuth()
  if (loading) return <div className="p-8 text-center">Loading...</div>
  if (!user) return <Navigate to="/login" />
  if (['official', 'admin'].includes(user.role)) return <Navigate to="/admin" />
  return <Navigate to="/dashboard" />
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/nearby"
        element={
        <ProtectedRoute>
          <NearbyFeed />
          </ProtectedRoute>
          }
      />
      <Route
        path="/admin"
        element={
          <ProtectedRoute requireStaff>
            <AdminDashboard />
          </ProtectedRoute>
        }
      />
      <Route path="/" element={<HomeRedirect />} />
      <Route path="*" element={<HomeRedirect />} />
    </Routes>
  )
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App