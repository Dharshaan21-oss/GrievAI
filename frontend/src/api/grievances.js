import apiClient from './client'

export const createGrievance = (data) => {
  return apiClient.post('/api/grievances/', data)
}

export const listGrievances = (params = {}) => {
  return apiClient.get('/api/grievances/', { params })
}

export const getGrievance = (id) => {
  return apiClient.get(`/api/grievances/${id}`)
}

export const updateGrievanceStatus = (id, data) => {
  return apiClient.patch(`/api/grievances/${id}/status`, data)
}
export const getStats = () => {
  return apiClient.get('/api/grievances/stats/summary')
}
export const getNearbyGrievances = (lat, lng, radiusKm) => {
  return apiClient.get('/api/grievances/nearby/feed', {
    params: { lat, lng, radius_km: radiusKm },
  })
}