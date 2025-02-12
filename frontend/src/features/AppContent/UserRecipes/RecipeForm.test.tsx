import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider } from '../../Themes/themeContext'
import RecipeForm from './RecipeForm'
import { findByTestId, render, screen } from '@testing-library/react'
import { mockRecipeTwo } from '../testVariables'
import userEvent from '@testing-library/user-event'

import { Provider } from 'react-redux'
import applicationStore from '../../../store'
const store = applicationStore()

// const ReduxProvider = ({ children, reduxStore }) => (
//   <Provider store={reduxStore}>{children}</Provider>
// )

jest.mock('../RecipeInformation/RecipeInfoSlice', () => ({
  useGetRecipeQuery: () => {
    return {
      data: mockRecipeTwo,
      isSuccess: true,
      isLoading: false,
    }
  },
}))

describe('Make sure images display and work', () => {
  test('Test Images Container Loads', async () => {
    render(
      <Provider store={store}>
        <BrowserRouter
          future={{
            v7_startTransition: true,
            v7_relativeSplatPath: true,
          }}
        >
          <ThemeProvider>
            <RecipeForm />
          </ThemeProvider>
        </BrowserRouter>
      </Provider>
    )
    // Shows tooltip
    const button = await screen.findByRole('button', {
      name: 'Click Image to Choose New Image',
    })

    // Tooltip displays text on hover
    await userEvent.hover(button)
    expect(await screen.findByRole('tooltip')).toBeInTheDocument()

    // Displays first image
    expect(screen.getByRole('img')).toBeInTheDocument

    // Displays pagination
    expect(screen.getByLabelText('pagination'))
    const imgPageination = screen.getByRole('list', { name: 'image-pagination' })
    expect(imgPageination).toBeInTheDocument()

    // Clicking on page 2 changes image
    const pageTwoBtn = screen.getByRole('button', {name: 'Go to page 2'})
    await userEvent.click(pageTwoBtn)


    // Displays Delete Image and Tooltip

    // Clicking Delete image shows different image

    // ...and removes one image from pagination

    // Displays Clear All and Tooltip

    // Clicking Clear All removes all images and shows Upload Image
  })
})

describe('Make sure images display and work', () => {})
