/*

Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com

*/

import React, { useState } from 'react'

import './Navbar.css'
import { useTheme } from '../../../Themes/themeContext'
import themes from '../../../Themes/themes'
import {
  AppBar,
  Box,
  Button,
  Grid2,
  Link,
  Menu,
  MenuItem,
  Popover,
  Stack,
  Toolbar,
} from '@mui/material'
import { KeyboardArrowDown } from '@mui/icons-material'
import { useAuth } from '../../Authentication/AuthProvider'
/**
 * File name: Navbar.tsx
 * Task - Home, About, Contact options available for the user on the Navigation Bar.
 * @author Asrita Kuchibhotla
 */

function Navbar() {
  const auth = useAuth()
  const { theme, toggleTheme } = useTheme()

  const [nextMealEl, setNextMealEl] = useState<null | HTMLElement>(null)
  const [mealPrepEl, setMealPrepEl] = useState<null | HTMLElement>(null)
  const [infoEl, setInfoEl] = useState<null | HTMLElement>(null)
  const [accountEl, setAccountEl] = useState<null | HTMLElement>(null)

  // Function to handle theme change
  const handleThemeChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    toggleTheme(event.target.value)
  }

  const CloseNextMealMenu = () => {
    setNextMealEl(null)
  }

  const CloseMealPrepMenu = () => {
    setMealPrepEl(null)
  }

  const CloseAboutMenu = () => {
    setInfoEl(null)
  }

  const CloseAccountMenu = () => {
    setAccountEl(null)
  }

  const handleLogout = () => {
    CloseAccountMenu()
    auth?.logOut()
  }

  return (
    // <section className="navbar" style={{ backgroundColor: theme.background }}>
    <Stack spacing={2} direction={'row'} data-testid="navbar">
      {/* <a href="/" className="navbar-item" style={{ color: theme.color }}>
        Home
      </a> */}
      <Button
        sx={{ color: theme.color }}
        id="your-next-meal"
        onClick={(e) => setNextMealEl(e.currentTarget)}
      >
        Your Next Meal
        <KeyboardArrowDown />
      </Button>
      <Button
        sx={{ color: theme.color }}
        id="meal-prep"
        onClick={(e) => setMealPrepEl(e.currentTarget)}
      >
        Meal Prep
        <KeyboardArrowDown />
      </Button>
      <Button
        sx={{ color: theme.color }}
        id="information"
        onClick={(e) => setInfoEl(e.currentTarget)}
      >
        Information
        <KeyboardArrowDown />
      </Button>

      <Button
        sx={{ color: theme.color }}
        id="account"
        onClick={(e) => setAccountEl(e.currentTarget)}
      >
        Account
        <KeyboardArrowDown />
      </Button>

      <Menu
        anchorEl={nextMealEl}
        open={Boolean(nextMealEl)}
        onClose={CloseNextMealMenu}
      >
        <Link underline="none" color="inherit" href="/feed">
          <MenuItem onClick={CloseNextMealMenu}>The Feed</MenuItem>
        </Link>

        <Link underline="none" color="inherit" href="/create-recipe">
          <MenuItem onClick={CloseNextMealMenu}>Create A Recipe </MenuItem>
        </Link>
      </Menu>
      <Menu
        anchorEl={mealPrepEl}
        open={Boolean(mealPrepEl)}
        onClose={CloseMealPrepMenu}
      >
        <Link underline="none" color="inherit" href="/meal">
          <MenuItem onClick={CloseMealPrepMenu}>Meal Plans</MenuItem>
        </Link>
        <Link underline="none" color="inherit" href="/shoppinglist">
          <MenuItem onClick={CloseMealPrepMenu}>Shopping Lists</MenuItem>
        </Link>
      </Menu>
      <Menu anchorEl={infoEl} open={Boolean(infoEl)} onClose={CloseAboutMenu}>
        <Link underline="none" color="inherit" href="/about">
          <MenuItem onClick={CloseAboutMenu}>About Us</MenuItem>
        </Link>

        <Link underline="none" color="inherit" href="/faq">
          <MenuItem onClick={CloseAboutMenu}>FAQS</MenuItem>
        </Link>
        <Link underline="none" color="inherit" href="/contact">
          <MenuItem onClick={CloseAboutMenu}>Contact Us</MenuItem>
        </Link>
      </Menu>

      <Menu
        anchorEl={accountEl}
        open={Boolean(accountEl)}
        onClose={CloseAccountMenu}
      >
        {auth?.userSignedIn ? (
          <Box>
            <Link underline="none" color="inherit" href="/profile">
              <MenuItem onClick={CloseAccountMenu}>Profile</MenuItem>
            </Link>
            <Button onClick={handleLogout}>
              <MenuItem onClick={CloseAccountMenu}>Log Out</MenuItem>
            </Button>
          </Box>
        ) : (
          <Box>
            <Link underline="none" color="inherit" href="/signup">
              <MenuItem onClick={CloseAccountMenu}>Sign Up</MenuItem>
            </Link>

            <Link underline="none" color="inherit" href="/login">
              <MenuItem onClick={CloseAccountMenu}>Log In</MenuItem>
            </Link>
          </Box>
        )}
      </Menu>
      {/* <a href="/meal" className="navbar-item" style={{ color: theme.color }}>
        Meal Plan
      </a>
      <a href="/about" className="navbar-item" style={{ color: theme.color }}>
        About
      </a>
      <a href="/faq" className="navbar-item" style={{ color: theme.color }}>
        FAQs
      </a>
      <a href="/contact" className="navbar-item" style={{ color: theme.color }}>
        Contact Us
      </a>
      <a href="/signup" className="navbar-item" style={{ color: theme.color }}>
        Signup
      </a> */}
      {/* <a
        href="/shoppinglist"
        className="navbar-item"
        style={{ color: theme.color }}
      >
        Shopping List
      </a> */}
      {/* Theme Dropdown */}

      <div className="theme-selector">
        <label htmlFor="theme-dropdown" style={{ color: theme.color }}>
          Select Theme:
        </label>
        <select
          id="theme-dropdown"
          onChange={handleThemeChange}
          value={Object.keys(themes).find(
            (themeName) =>
              themes[themeName as keyof typeof themes].background ===
              theme.background
          )}
          style={{
            backgroundColor: theme.background,
            color: theme.color,
            cursor: 'pointer',
            border: `1px solid ${theme.color}`,
          }}
        >
          {Object.keys(themes).map((themeName) => (
            <option
              key={themeName}
              value={themeName}
              style={{
                backgroundColor:
                  themes[themeName as keyof typeof themes].background,
                color: themes[themeName as keyof typeof themes].color,
              }}
            >
              {themeName}
            </option>
          ))}
        </select>
      </div>
    </Stack>

    // </section>
  )
}

export default Navbar
