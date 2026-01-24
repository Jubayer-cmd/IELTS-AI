import { createContext, useContext, useEffect, useMemo, useState, useRef } from 'react'

const ThemeContext = createContext()

const COLOR_THEMES = ['violet', 'indigo', 'emerald', 'rose', 'amber']

function applyThemeClass(theme) {
  const root = document.documentElement
  COLOR_THEMES.forEach((name) => root.classList.remove(`theme-${name}`))
  root.classList.add(`theme-${theme}`)
}

export default function ThemeProvider({ children }) {
  const [primary, setPrimary] = useState(() => {
    // Initialize from localStorage
    const saved = localStorage.getItem('theme-primary')
    if (saved && COLOR_THEMES.includes(saved)) {
      return saved
    }
    return 'violet'
  })

  const isInitialMount = useRef(true)

  // Apply theme class on mount
  useEffect(() => {
    applyThemeClass(primary)
  }, [])

  // Apply theme and save when primary changes (but not on initial mount)
  useEffect(() => {
    if (isInitialMount.current) {
      isInitialMount.current = false
      return
    }

    applyThemeClass(primary)
    localStorage.setItem('theme-primary', primary)
  }, [primary])

  const value = useMemo(() => ({ primary, setPrimary, options: COLOR_THEMES }), [primary])

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}

export function useTheme() {
  const ctx = useContext(ThemeContext)
  if (!ctx) throw new Error('useTheme must be used within ThemeProvider')
  return ctx
}
