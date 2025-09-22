// Main React application component
// TODO: Implement routing, authentication, and main layout

import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './services/auth'
import ThemeProvider from '@/context/ThemeProvider'
import Sidebar from '@/components/Chat/Sidebar'
import MobileSidebar from '@/components/Chat/MobileSidebar'
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
  const [isMobile, setIsMobile] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [collapsed, setCollapsed] = useState(false)

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768)
    }

    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  if (!isAuthenticated) {
    return (
      <div className="h-screen w-screen bg-background dark">
        {isMobile ? (
          <MobileLayout />
        ) : (
          <DesktopLayout />
        )}
      </div>
    )
  }

  return (
    <div className="h-screen w-screen bg-background dark">
      {isMobile ? (
        <MobileLayout />
      ) : (
        <DesktopLayout />
      )}
    </div>
  )
}

function DesktopLayout() {
  const [collapsed, setCollapsed] = useState(false)
  return (
    <div className="flex h-full">
      <div className={`${collapsed ? 'w-16' : 'w-64'} h-full transition-all duration-300 border-r border-border`}>
        <Sidebar collapsed={collapsed} onToggle={() => setCollapsed(!collapsed)} />
      </div>
      <main className="flex-1 h-full flex flex-col overflow-hidden">
        <Routes>
          <Route path="/" element={<HomePage />} />
        </Routes>
      </main>
    </div>
  )
}

function MobileLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  return (
    <div className="flex flex-col h-full">
      <MobileSidebar open={sidebarOpen} onOpenChange={setSidebarOpen} />
      <main className="flex-1 flex flex-col overflow-hidden">
        <Routes>
          <Route path="/" element={<HomePage onMenuClick={() => setSidebarOpen(true)} />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
