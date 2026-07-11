import { useAuth } from '../context/AuthContext'

export default function Dashboard() {
  const { user, logout } = useAuth()

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-2xl mx-auto bg-white rounded-xl shadow p-6">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold text-blue-600">Welcome, {user?.full_name}</h1>
          <button
            onClick={logout}
            className="text-sm text-red-600 hover:underline"
          >
            Logout
          </button>
        </div>
        <p className="text-gray-600">Role: {user?.role}</p>
        <p className="text-gray-600">Email: {user?.email}</p>
        <p className="text-gray-400 mt-4 text-sm">
          (Grievance form and list will go here in the next task)
        </p>
      </div>
    </div>
  )
}