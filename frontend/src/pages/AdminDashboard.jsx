import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { listGrievances, getStats } from '../api/grievances'
import { PriorityBadge, StatusBadge } from '../components/Badge'
import StatusUpdateSelect from '../components/StatusUpdateSelect'
import StatCard from '../components/StatCard'

export default function AdminDashboard() {
  const { user, logout } = useAuth()
  const [grievances, setGrievances] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('')

  const fetchData = async () => {
    setLoading(true)
    try {
      const params = {}
      if (statusFilter) params.status = statusFilter
      if (categoryFilter) params.category = categoryFilter

      const [grievancesRes, statsRes] = await Promise.all([
        listGrievances(params),
        getStats(),
      ])
      setGrievances(grievancesRes.data)
      setStats(statsRes.data)
    } catch (err) {
      console.error('Failed to fetch admin data', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusFilter, categoryFilter])

  const handleStatusUpdated = (updated) => {
    setGrievances(grievances.map((g) => (g.id === updated.id ? updated : g)))
  }

  const categories = stats?.by_category?.map((c) => c.category) || []

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-blue-600">GrievAI — Admin Panel</h1>
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

      <main className="max-w-6xl mx-auto px-6 py-8">
        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
            <StatCard label="Total Grievances" value={stats.total} accent="text-blue-600" />
            <StatCard label="Resolved" value={stats.resolved} accent="text-green-600" />
            <StatCard label="Critical Issues" value={stats.critical} accent="text-red-600" />
          </div>
        )}

        {/* Filters */}
        <div className="flex gap-3 mb-4">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="text-sm border border-gray-300 rounded-lg px-3 py-2"
          >
            <option value="">All Statuses</option>
            <option value="filed">Filed</option>
            <option value="in_review">In Review</option>
            <option value="assigned">Assigned</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
            <option value="rejected">Rejected</option>
          </select>
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="text-sm border border-gray-300 rounded-lg px-3 py-2"
          >
            <option value="">All Categories</option>
            {categories.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>

        {/* Table */}
        <div className="bg-white rounded-xl shadow overflow-hidden">
          {loading ? (
            <div className="text-center text-gray-500 py-8">Loading...</div>
          ) : grievances.length === 0 ? (
            <div className="text-center text-gray-400 py-8">No grievances found.</div>
          ) : (
            <table className="w-full text-sm">
              <thead className="bg-gray-50 text-gray-600 text-left">
                <tr>
                  <th className="px-4 py-3">Title</th>
                  <th className="px-4 py-3">Category</th>
                  <th className="px-4 py-3">Priority</th>
                  <th className="px-4 py-3">Status</th>
                  <th className="px-4 py-3">Filed</th>
                  <th className="px-4 py-3">Update Status</th>
                </tr>
              </thead>
              <tbody>
                {grievances.map((g) => (
                  <tr key={g.id} className="border-t border-gray-100">
                    <td className="px-4 py-3 font-medium text-gray-800">
                      {g.title}
                      {g.is_duplicate && (
                        <span className="ml-2 text-xs text-orange-600">
                          (dup of #{g.duplicate_of_id})
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-gray-600">{g.category || '—'}</td>
                    <td className="px-4 py-3"><PriorityBadge priority={g.priority} /></td>
                    <td className="px-4 py-3"><StatusBadge status={g.status} /></td>
                    <td className="px-4 py-3 text-gray-500">
                      {new Date(g.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-4 py-3">
                      <StatusUpdateSelect grievance={g} onUpdated={handleStatusUpdated} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </main>
    </div>
  )
}