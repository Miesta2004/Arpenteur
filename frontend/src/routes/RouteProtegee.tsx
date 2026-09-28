import { Navigate, Outlet } from 'react-router-dom'
import { isAuthenticated } from '@/api/client'

export default function RouteProtegee() {
  if (!isAuthenticated()) {
    return <Navigate to="/connexion" replace />
  }
  return <Outlet />
}
