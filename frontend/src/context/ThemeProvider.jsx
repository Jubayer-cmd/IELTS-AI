import { createContext, useContext, useEffect, useMemo, useState } from 'react'

const ThemeContext = createContext()

const COLOR_THEMES = ['violet', 'indigo', 'emerald', 'rose', 'amber']

function applyThemeClass(theme) {
  const root = document.documentElement
  COLOR_THEMES.forEach((name) => root.classList.remove(`theme-${name}`))
  root.classList.add(`theme-${theme}`)
}

export default function ThemeProvider({ children }) {
  const [primary, setPrimary] = useState('violet')

  useEffect(() => {
    const saved = localStorage.getItem('theme-primary')
    if (saved && COLOR_THEMES.includes(saved)) {
      setPrimary(saved)
      applyThemeClass(saved)
    } else {
      applyThemeClass('violet')
    }
  }, [])

  useEffect(() => {
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


