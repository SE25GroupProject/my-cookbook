/*

Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com

*/

/**
 * File name: App.tsx
 * Task - This is the parent component of the application. It creates the basic UI skeleton
 * viz the header, the search component and the app contents
 * Header and Search component remain static and app contents change according to the state of the application
 * @author Priyanka Ambawane - dearpriyankasa@gmail.com
 */
import React, { useState } from 'react'
import { Provider } from 'react-redux'
import { BrowserRouter } from 'react-router-dom'
import applicationStore from './store'
import './App.css'
import GetIngredients from './features/GetIngredients/GetIngredients'
import Header from './features/Header/Header'
import AppContent from './features/AppContent/AppContent'
import GetTags from './features/AppContent/Tag/GetTags'
import CustomizedAccordions from './features/AppContent/NutritionFilter/CustomizedAccordions'
import { ThemeProvider, useTheme } from './features/Themes/themeContext'
import Login from './features/AppContent/HomePage/Login'
import Profile from './features/AppContent/HomePage/Profile'
import { Button } from '@mui/material'
import { FaAngleDoubleDown, FaAngleDoubleUp } from 'react-icons/fa'

const store = applicationStore()

// Separate function for the main application content
const AppContentLayout: React.FC = () => {
  const { theme } = useTheme()
  const [searchOpen, setSearchOpen] = useState(false)

  const toggleSearchBar = () => {
    setSearchOpen(!searchOpen)
  }

  return (
    <div
      className="App"
      style={{ backgroundColor: theme.background, color: theme.color }}
    >
      <div
        className="App-header"
        data-testid="header-comp-43"
        style={{ backgroundColor: theme.background }}
      >
        <Header />
      </div>
      <div className="search-bar-container">
        <div className={`search-bar ${searchOpen ? '' : 'hidden'}`}>
          <div
            className="search-helper"
            data-testid="search-comp-43"
            style={{ backgroundColor: theme.background }}
          >
            <GetIngredients />
          </div>
          <div
            className="search-helper"
            data-testid="header-comp-44"
            style={{ backgroundColor: theme.background }}
          >
            <GetTags />
          </div>
          <div
            className="search-helper"
            data-testid="header-comp-45"
            style={{ backgroundColor: theme.background }}
          >
            <CustomizedAccordions />
          </div>
        </div>
        <div className="search-expand">
          <Button onClick={toggleSearchBar}>
            {searchOpen ? (
              <FaAngleDoubleUp fontSize={24} color={theme.color} />
            ) : (
              <FaAngleDoubleDown fontSize={24} color={theme.color} />
            )}
          </Button>
        </div>
      </div>
      <div
        className="App-body"
        data-testid="body-comp-43"
        style={{ backgroundColor: theme.background }}
      >
        <AppContent />
      </div>
    </div>
  )
}

// Main App component
const App: React.FC = () => {
  return (
    <Provider store={store}>
      <BrowserRouter
        future={{
          v7_relativeSplatPath: true,
          v7_startTransition: true,
        }}
      >
        <ThemeProvider>
          <AppContentLayout />
        </ThemeProvider>
      </BrowserRouter>
    </Provider>
  )
}

export default App
