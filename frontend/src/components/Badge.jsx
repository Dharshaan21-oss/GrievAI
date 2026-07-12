const PRIORITY_STYLES = {
  critical: 'bg-red-100 text-red-700',
  high: 'bg-orange-100 text-orange-700',
  medium: 'bg-yellow-100 text-yellow-700',
  low: 'bg-green-100 text-green-700',
}

const STATUS_STYLES = {
  filed: 'bg-gray-100 text-gray-700',
  in_review: 'bg-blue-100 text-blue-700',
  assigned: 'bg-purple-100 text-purple-700',
  in_progress: 'bg-indigo-100 text-indigo-700',
  resolved: 'bg-green-100 text-green-700',
  rejected: 'bg-red-100 text-red-700',
}

export function PriorityBadge({ priority }) {
  const style = PRIORITY_STYLES[priority] || 'bg-gray-100 text-gray-700'
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium capitalize ${style}`}>
      {priority}
    </span>
  )
}

export function StatusBadge({ status }) {
  const style = STATUS_STYLES[status] || 'bg-gray-100 text-gray-700'
  const label = status.replace('_', ' ')
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium capitalize ${style}`}>
      {label}
    </span>
  )
}