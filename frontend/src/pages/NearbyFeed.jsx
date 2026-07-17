import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getNearbyGrievances } from '../api/grievances'
import { PriorityBadge, StatusBadge } from '../components/Badge'

const RADIUS_OPTIONS = [1, 3, 5, 10]

export default function NearbyFeed() {
  const [location, setLocation] = useState(null)
  const [radius, setRadius] = useState(5)
  const [grievances, setGrievances] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser')
      setLoading(false)
      return
    }
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        })
      },
      () => {
        setError('Location permission denied. Enable it to see nearby issues.')
        setLoading(false)
      }
    )
  }, [])

  useEffect(() => {
    if (!location) return
    setLoading(true)
    getNearbyGrievances(location.lat, location.lng, radius)
      .then((res) => setGrievances(res.data))
      .catch(() => setError('Failed to load nearby grievances'))
      .finally(() => setLoading(false))
  }, [location, radius])

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-blue-600">GrievAI — Nearby Issues</h1>
          <Link to="/dashboard" className="text-sm text-blue-600 hover:underline">
            My Dashboard
          </Link>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8">
        <div className="flex items-center gap-2 mb-6">
          <span className="text-sm text-gray-600">Radius:</span>
          {RADIUS_OPTIONS.map((r) => (
            <button
              key={r}
              onClick={() => setRadius(r)}
              className={`px-3 py-1.5 rounded-full text-sm font-medium transition ${
                radius === r
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-600 border border-gray-300'
              }`}
            >
              {r} km
            </button>
          ))}
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 text-sm p-4 rounded-lg mb-4">{error}</div>
        )}

        {loading ? (
          <div className="text-center text-gray-500 py-8">Loading nearby issues...</div>
        ) : grievances.length === 0 && !error ? (
          <div className="text-center text-gray-400 py-8 bg-white rounded-xl shadow">
            No issues reported within {radius} km yet.
          </div>
        ) : (
          <div className="space-y-4">
            {grievances.map((g) => (
              <div key={g.id} className="bg-white rounded-xl shadow p-5">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold text-gray-800">{g.title}</h3>
                  <div className="flex gap-2">
                    <PriorityBadge priority={g.priority} />
                    <StatusBadge status={g.status} />
                  </div>
                </div>
                <p className="text-sm text-gray-600 mb-2">{g.ai_summary || g.description}</p>
                <div className="flex flex-wrap gap-3 text-xs text-gray-500">
                  {g.category && <span>Category: <span className="font-medium">{g.category}</span></span>}
                  {g.location && <span>📍 {g.location}</span>}
                  <span>Filed: {new Date(g.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}