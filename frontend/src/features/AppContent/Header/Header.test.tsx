/*

Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com

*/

import React from 'react'
import {
  getByDisplayValue,
  getByLabelText,
  getByTitle,
  render,
  screen,
} from '@testing-library/react'
import Header from './Header'
import { ThemeProvider } from '../../Themes/themeContext'

test('shows header correctly', () => {
  const { getByText } = render(
    <ThemeProvider>
      <Header />
    </ThemeProvider>
  )
  expect(getByText('C o o k B o o k')).toBeInTheDocument()
})

test('has navbar component ', () => {
  const { getByTestId } = render(
    <ThemeProvider>
      <Header />
    </ThemeProvider>
  )
  expect(getByTestId('nav-comp-43')).toBeInTheDocument()
})
