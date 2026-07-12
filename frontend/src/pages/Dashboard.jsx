import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { listGrievances } from '../api/grievances'
import GrievanceForm from '../components/GrievanceForm'
import GrievanceList from '../components/GrievanceList'

export default function Dashboard() {
  const { user, logout } = useAuth()
  const [grievances, setGrievances] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchGrievances = async () => {
    setLoading(true)
    try {
      const res = await listGrievances()
      setGrievances(res.data)
    } catch (err) {
      console.error('Failed to fetch grievances', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchGrievances()
  }, [])

  const handleCreated = (newGrievance) => {
    setGrievances([newGrievance, ...grievances])
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-5xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-blue-600">GrievAI</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">
              {user?.full_name} <span className="text-gray-400">({user?.role})</span>
            </span>
            <button onClick={logout} className="text-sm text-red-600 hover:underline">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-8 grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <GrievanceForm onCreated={handleCreated} />
        </div>
        <div>
          <h2 className="text-lg font-bold text-gray-800 mb-4">My Grievances</h2>
          <GrievanceList grievances={grievances} loading={loading} />
        </div>
      </main>
    </div>
  )
}