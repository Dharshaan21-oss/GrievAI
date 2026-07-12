import { useState } from 'react'
import { updateGrievanceStatus } from '../api/grievances'

const STATUS_OPTIONS = ['filed', 'in_review', 'assigned', 'in_progress', 'resolved', 'rejected']

export default function StatusUpdateSelect({ grievance, onUpdated }) {
  const [updating, setUpdating] = useState(false)

  const handleChange = async (e) => {
    const newStatus = e.target.value
    if (newStatus === grievance.status) return
    setUpdating(true)
    try {
      const res = await updateGrievanceStatus(grievance.id, { status: newStatus })
      onUpdated(res.data)
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to update status')
    } finally {
      setUpdating(false)
    }
  }

  return (
    <select
      value={grievance.status}
      onChange={handleChange}
      disabled={updating}
      className="text-xs border border-gray-300 rounded-lg px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
    >
      {STATUS_OPTIONS.map((s) => (
        <option key={s} value={s}>
          {s.replace('_', ' ')}
        </option>
      ))}
    </select>
  )
}