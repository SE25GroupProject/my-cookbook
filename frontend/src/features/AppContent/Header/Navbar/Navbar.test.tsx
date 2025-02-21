import React from 'react'
import {
  getByDisplayValue,
  getByLabelText,
  getByTitle,
  render,
  screen,
} from '@testing-library/react'
/*

Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com

*/

import Navbar from './Navbar'
import { ThemeProvider } from '../../../Themes/themeContext'
import userEvent from '@testing-library/user-event'

test('shows Next Meal links in Navbar', async () => {
  render(
    <ThemeProvider>
      <Navbar />
    </ThemeProvider>
  )
  const nextMeal = screen.getByText('Your Next Meal')

  userEvent.click(nextMeal)

  expect(await screen.findByText('Create A Recipe')).toBeInTheDocument()
  expect(screen.getByText('The Feed')).toBeInTheDocument()
})

test('shows Meal Prep links in Navbar', async () => {
  render(
    <ThemeProvider>
      <Navbar />
    </ThemeProvider>
  )

  const mealPrep = screen.getByText('Meal Prep')

  userEvent.click(mealPrep)

  expect(await screen.findByText('Shopping Lists')).toBeInTheDocument()
  expect(screen.getByText('Meal Plans')).toBeInTheDocument()
})

test('shows Info links in Navbar', async () => {
  render(
    <ThemeProvider>
      <Navbar />
    </ThemeProvider>
  )

  const info = screen.getByText('Information')

  userEvent.click(info)

  expect(
    await screen.findByText(/About Us/i, { exact: false })
  ).toBeInTheDocument()

  expect(screen.getByText(/Contact/i, { exact: false })).toBeInTheDocument()
  expect(screen.getByText(/FAQ/i, { exact: false })).toBeInTheDocument()
})

test('shows Account links in Navbar', async () => {
  render(
    <ThemeProvider>
      <Navbar />
    </ThemeProvider>
  )

  const account = screen.getByText('Account')

  userEvent.click(account)

  expect(
    await screen.findByText(/Sign Up/i, { exact: false })
  ).toBeInTheDocument()

  expect(screen.getByText(/Log In/i, { exact: false })).toBeInTheDocument()
})

test('shows Select Theme Dropdown in Navbar', () => {
  render(
    <ThemeProvider>
      <Navbar />
    </ThemeProvider>
  )
  expect(screen.getByText(/Select Theme:/i)).toBeInTheDocument()
})
