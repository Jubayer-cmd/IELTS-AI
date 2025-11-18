import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './services/auth'
import ThemeProvider from '@/context/ThemeProvider'
import Sidebar from '@/components/Chat/Sidebar'
import MobileSidebar from '@/components/Chat/MobileSidebar'
import HomePage from '@/pages/HomePage'
import { useAuth } from '@/services/auth'
import { chatAPI } from '@/services/api'

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
  const [threads, setThreads] = useState([])
  const [currentThreadId, setCurrentThreadId] = useState(null)
  const [isLoadingThreads, setIsLoadingThreads] = useState(true)

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768)
    }

    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  // Load threads on mount
  useEffect(() => {
    loadThreads()
  }, [])

  const loadThreads = async () => {
    try {
      setIsLoadingThreads(true)
      const fetchedThreads = await chatAPI.getThreads()
      setThreads(fetchedThreads)

      // If no current thread and threads exist, select the first one
      if (!currentThreadId && fetchedThreads.length > 0) {
        setCurrentThreadId(fetchedThreads[0].id)
      } else if (fetchedThreads.length === 0) {
        // If no threads exist, create one automatically
        const newThread = await chatAPI.createThread('New Chat')
        setThreads([newThread])
        setCurrentThreadId(newThread.id)
      }
    } catch (error) {
      console.error('Failed to load threads:', error)
    } finally {
      setIsLoadingThreads(false)
    }
  }

  const handleNewThread = async () => {
    try {
      const newThread = await chatAPI.createThread('New Chat')
      setThreads([newThread, ...threads])
      setCurrentThreadId(newThread.id)
    } catch (error) {
      console.error('Failed to create thread:', error)
    }
  }

  const handleSelectThread = (threadId) => {
    setCurrentThreadId(threadId)
  }

  const handleDeleteThread = async (threadId) => {
    try {
      await chatAPI.deleteThread(threadId)

      // Remove thread from state
      const updatedThreads = threads.filter(t => t.id !== threadId)
      setThreads(updatedThreads)

      // If deleted thread was selected, switch to another thread
      if (currentThreadId === threadId) {
        if (updatedThreads.length > 0) {
          setCurrentThreadId(updatedThreads[0].id)
        } else {
          // No threads left, create a new one
          const newThread = await chatAPI.createThread('New Chat')
          setThreads([newThread])
          setCurrentThreadId(newThread.id)
        }
      }
    } catch (error) {
      console.error('Failed to delete thread:', error)
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="h-screen w-screen bg-background dark">
        {isMobile ? (
          <MobileLayout
            threads={threads}
            currentThreadId={currentThreadId}
            onSelectThread={handleSelectThread}
            onNewThread={handleNewThread}
            onDeleteThread={handleDeleteThread}
            sidebarOpen={sidebarOpen}
            setSidebarOpen={setSidebarOpen}
          />
        ) : (
          <DesktopLayout
            threads={threads}
            currentThreadId={currentThreadId}
            onSelectThread={handleSelectThread}
            onNewThread={handleNewThread}
            onDeleteThread={handleDeleteThread}
            collapsed={collapsed}
            setCollapsed={setCollapsed}
          />
        )}
      </div>
    )
  }

  return (
    <div className="h-screen w-screen bg-background dark">
      {isMobile ? (
        <MobileLayout
          threads={threads}
          currentThreadId={currentThreadId}
          onSelectThread={handleSelectThread}
          onNewThread={handleNewThread}
          onDeleteThread={handleDeleteThread}
          sidebarOpen={sidebarOpen}
          setSidebarOpen={setSidebarOpen}
        />
      ) : (
        <DesktopLayout
          threads={threads}
          currentThreadId={currentThreadId}
          onSelectThread={handleSelectThread}
          onNewThread={handleNewThread}
          onDeleteThread={handleDeleteThread}
          collapsed={collapsed}
          setCollapsed={setCollapsed}
        />
      )}
    </div>
  )
}

function DesktopLayout({ threads, currentThreadId, onSelectThread, onNewThread, onDeleteThread, collapsed, setCollapsed }) {
  return (
    <div className="flex h-full">
      <div className={`${collapsed ? 'w-16' : 'w-64'} h-full transition-all duration-300 border-r border-border`}>
        <Sidebar
          collapsed={collapsed}
          onToggle={() => setCollapsed(!collapsed)}
          threads={threads}
          currentThreadId={currentThreadId}
          onSelectThread={onSelectThread}
          onNewThread={onNewThread}
          onDeleteThread={onDeleteThread}
        />
      </div>
      <main className="flex-1 h-full flex flex-col overflow-hidden">
        <Routes>
          <Route path="/" element={<HomePage currentThreadId={currentThreadId} />} />
        </Routes>
      </main>
    </div>
  )
}

function MobileLayout({ threads, currentThreadId, onSelectThread, onNewThread, onDeleteThread, sidebarOpen, setSidebarOpen }) {
  return (
    <div className="flex flex-col h-full">
      <MobileSidebar
        open={sidebarOpen}
        onOpenChange={setSidebarOpen}
        threads={threads}
        currentThreadId={currentThreadId}
        onSelectThread={onSelectThread}
        onNewThread={onNewThread}
        onDeleteThread={onDeleteThread}
      />
      <main className="flex-1 flex flex-col overflow-hidden">
        <Routes>
          <Route path="/" element={<HomePage onMenuClick={() => setSidebarOpen(true)} currentThreadId={currentThreadId} />} />
        </Routes>
      </main>
    </div>
  )
}

export default App

