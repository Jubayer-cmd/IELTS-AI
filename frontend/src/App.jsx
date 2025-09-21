// Main React application component
// TODO: Implement routing, authentication, and main layout

import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './services/auth'
import ThemeProvider from '@/context/ThemeProvider'
import Sidebar from '@/components/Chat/Sidebar'
import HomePage from '@/pages/HomePage'
import { useAuth } from '@/services/auth'

// TODO: Import components
// import LoginPage from './pages/LoginPage'
// import RegisterPage from './pages/RegisterPage'
// import EvaluationPage from './pages/EvaluationPage'
// import DashboardPage from './pages/DashboardPage'
// import AdminPage from './pages/AdminPage'

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <Shell />
        </Router>
      </AuthProvider>
    </ThemeProvider>
  )
}

function Shell() {
  const { isAuthenticated } = useAuth()
  if (!isAuthenticated) {
  return (
    <div className="h-screen w-screen bg-background dark overflow-hidden flex">
      <CollapsibleSidebar />
      <main className="flex-1 h-full flex flex-col">
        <HomePage />
      </main>
    </div>
  )
  }

  return (
    <div className="h-screen w-screen bg-background dark overflow-hidden flex">
      <CollapsibleSidebar />
      <main className="flex-1 h-full flex flex-col">
        <Routes>
          <Route path="/" element={<HomePage />} />
        </Routes>
      </main>
    </div>
  )
}

function CollapsibleSidebar() {
  const [collapsed, setCollapsed] = useState(false)
  return (
    <div className={`${collapsed ? 'w-16' : 'w-64'} h-full transition-all duration-300 border-r border-border`}>
      <Sidebar collapsed={collapsed} onToggle={() => setCollapsed(!collapsed)} />
    </div>
  )
}

export default App
