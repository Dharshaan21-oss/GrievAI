import { PriorityBadge, StatusBadge } from './Badge'

export default function GrievanceList({ grievances, loading }) {
  if (loading) {
    return <div className="text-center text-gray-500 py-8">Loading grievances...</div>
  }

  if (grievances.length === 0) {
    return (
      <div className="text-center text-gray-400 py-8 bg-white rounded-xl shadow">
        No grievances filed yet.
      </div>
    )
  }

  return (
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
          <p className="text-sm text-gray-600 mb-3">{g.description}</p>
          {g.ai_summary && g.ai_summary !== g.description && (
            <div className="bg-blue-50 border-l-4 border-blue-400 p-3 rounded mb-3">
              <p className="text-xs font-medium text-blue-700 mb-1">AI Summary</p>
              <p className="text-sm text-blue-900">{g.ai_summary}</p>
            </div>
          )}
          <div className="flex flex-wrap gap-3 text-xs text-gray-500">
            {g.category && (
              <span>
                Category: <span className="font-medium text-gray-700">{g.category}</span>
                {g.category_confidence && ` (${(g.category_confidence * 100).toFixed(0)}%)`}
              </span>
            )}
            {g.location && <span>Location: {g.location}</span>}
            {g.is_duplicate && (
              <span className="text-orange-600 font-medium">
                ⚠ Marked as duplicate of #{g.duplicate_of_id}
              </span>
            )}
            <span>Filed: {new Date(g.created_at).toLocaleDateString()}</span>
          </div>
        </div>
      ))}
    </div>
  )
}