import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import RouteProtegee from '@/routes/RouteProtegee'
import EcranConnexion from '@/pages/EcranConnexion'
import TableauDeBord from '@/pages/TableauDeBord'
import ListeEtablissements from '@/pages/ListeEtablissements'
import DetailEtablissement from '@/pages/DetailEtablissement'
import DetailVisite from '@/pages/DetailVisite'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, refetchOnWindowFocus: false },
  },
})

export default function App() {
  return (
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Routes>
            <Route path="/connexion" element={<EcranConnexion />} />

            <Route element={<RouteProtegee />}>
              <Route path="/" element={<Navigate to="/tableau-de-bord" replace />} />
              <Route path="/tableau-de-bord" element={<TableauDeBord />} />
              <Route path="/etablissements" element={<ListeEtablissements />} />
              <Route path="/etablissements/:id" element={<DetailEtablissement />} />
              <Route path="/visites/:id" element={<DetailVisite />} />
            </Route>

            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
  )
}
