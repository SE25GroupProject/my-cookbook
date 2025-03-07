import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider } from '../../Themes/themeContext'
import SocialMedia from './SocialMedia'
import userEvent from '@testing-library/user-event'
import { renderWithProviders } from '../../../utils/testingUtils'
import { testPosts } from '../testVariables'
import { http, HttpResponse } from 'msw'
import { server } from '../../api/msw'

beforeAll(() => server.listen())
afterEach(() => {
  server.resetHandlers()
})
afterAll(() => {
  server.close()
})

describe('Display Social Media Page Items', () => {
  test('Ensure Posts are visible', async () => {
    await renderWithProviders(<SocialMedia />)

    await waitFor(() => {
      const headings = screen.getAllByRole('heading', {
        level: 6,
        name: 'Recipe Title',
      })

      headings.forEach((heading, index) => {
        expect(heading).toHaveTextContent(`Test ${index + 1}`)
      })
    })

    const postImages = screen.queryAllByRole('image', { name: 'Post Image' })

    postImages.forEach((image) => {
      expect(image).toBeInTheDocument()
    })

    const postContents = screen.getAllByRole('paragraph', {
      name: 'Post Content',
    })

    postContents.forEach((content) => {
      expect(content).toBeInTheDocument()
    })
  })

  test.skip('Ensure Post Comments are visible', async () => {
    await renderWithProviders(<SocialMedia />)
  })

  test('Ensure Update Text Box is visible', async () => {
    await renderWithProviders(<SocialMedia />)

    expect(
      await screen.findByRole('textbox', { name: "What's Cookin'?" })
    ).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Submit Recipe' })).toBeDisabled()
  })

  test('Ensure Recipe Dropdown is visible', async () => {
    await renderWithProviders(<SocialMedia />)

    expect(
      screen.getByRole('combobox', { name: 'Your Recipes' })
    ).toBeInTheDocument()
  })

  test('Ensure Image Modal can be viewed', async () => {
    await renderWithProviders(<SocialMedia />)

    const imgBtn = screen.getByLabelText(/Click to Change Image/i)
    expect(screen.getByAltText(/Recipe Image/i)).toBeInTheDocument()

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
})

describe('Test Social Media Page Functionality', () => {
  test.skip('Test Creating a Post', () => {})

  test.skip('Test Liking a Post (And Undo)', () => {})

  test.skip('Test Disliking a Post (And Undo)', () => {})

  test.skip('Test Making a Comment', () => {})

  test.skip('Test Deleting a Comment', () => {})
})
