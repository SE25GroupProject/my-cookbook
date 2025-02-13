/*

Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com

*/

import React from 'react'
import './Header.css'
import Navbar from '../Navbar/Navbar'
import { useTheme } from '../Themes/themeContext'
import { AppBar, Divider, Link, Toolbar, Typography } from '@mui/material'
import { MenuBook } from '@mui/icons-material'
/**
 * File name: Header.tsx
 * Functional component displaying the top navigation bar.
 * Task - This component is responsible for the static header seen throughout the application with the option to navigate back to home
 * and provides 'Contact' and 'About' information.
 * @author Asrita Kuchibhotla
 */

const Header = () => {
  const { theme } = useTheme()
  return (
    // <section
    //   className="header"
    //   style={{ backgroundColor: theme.background, color: theme.color }}
    // >

    <AppBar sx={{ background: theme.background }}>
      <Toolbar>
        {/* <section className="header-top"> */}
        {/* <section className="header-top__logo"> */}
        <Typography
          variant="h1"
          component="div"
          sx={{ flexGrow: 1, fontFamily: 'RobotoThin' }}
          textAlign="left"
        >
          <Link underline="none" href="/" sx={{ color: theme.headerColor }}>
            C o o k B o o k
          </Link>
        </Typography>

        <Divider />
        {/* </section> */}
        <Navbar />
        {/* <section className="header-top__navbar" data-testid="nav-comp-43">
          <section className="header-top__navigation">
            
          </section>
          <hr className="header-top__seperator" />
        </section> */}
        {/* </section> */}
      </Toolbar>
    </AppBar>
  )
}

export default Header
