import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider } from '../../Themes/themeContext'
import Profile from './Profile'
import userEvent from '@testing-library/user-event'
import { renderWithProviders } from '../../../utils/testingUtils'

describe('Display Profile Page Items', () => {
  test('Ensure Name is visible', async () => {
    await renderWithProviders(<Profile />)

    expect(
      screen.getByRole('heading', { level: 3, name: 'Users Name' })
    ).toBeInTheDocument()
  })

  test('Ensure Profile Image and Upload is visible', async () => {
    await renderWithProviders(<Profile />)

    const imgBtn = screen.getByLabelText(/Click to Change Image/i)
    expect(screen.getByAltText(/Profile/i)).toBeInTheDocument()

    await userEvent.click(imgBtn)

    expect(screen.getByText(/Upload An Image/i)).toBeInTheDocument()
    expect(
      screen.getByRole('button', {
        name: 'Delete Current Image',
      })
    ).toBeInTheDocument()
    expect(
      screen.getByRole('button', {
        name: 'Delete All Images',
      })
    ).toBeInTheDocument()
  })

  test('Ensure Profile tabs are visible', async () => {
    await renderWithProviders(<Profile />)

    expect(screen.getByRole('tab', { name: 'My Posts' })).toBeInTheDocument()
    expect(
      screen.getByRole('tab', { name: 'My Favorites' })
    ).toBeInTheDocument()
    expect(screen.getByRole('tab', { name: 'My Recipes' })).toBeInTheDocument()
  })
})
