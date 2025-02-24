import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider } from '../../Themes/themeContext'
import SocialMedia from './SocialMedia'
import userEvent from '@testing-library/user-event'

describe('Display Social Media Page Items', () => {
  test('Ensure Posts are visible', async () => {
    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <SocialMedia />
        </ThemeProvider>
      </BrowserRouter>
    )

    const headings = screen.getAllByRole('heading', {
      level: 6,
      name: 'Recipe Title',
    })

    headings.forEach((heading) => {
      expect(heading).toHaveTextContent(/Recipe/i)
    })

    const postImages = screen.getAllByRole('image', { name: 'Post Image' })

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

  test.skip('Ensure Post Comments are visible', () => {
    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <SocialMedia />
        </ThemeProvider>
      </BrowserRouter>
    )
  })

  test('Ensure Update Text Box is visible', () => {})

  test('Ensure Recipe Dropdown is visible', () => {})

  test('Ensure Image Modal can be viewed', async () => {
    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <SocialMedia />
        </ThemeProvider>
      </BrowserRouter>
    )

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

  test('Ensure Submit Post is visible', () => {})
})

describe('Test Social Media Page Functionality', () => {
  test('Test Creating a Post', () => {})

  test('Test Liking a Post (And Undo)', () => {})

  test('Test Disliking a Post (And Undo)', () => {})

  test('Test Making a Comment', () => {})

  test('Test Deleting a Comment', () => {})
})
