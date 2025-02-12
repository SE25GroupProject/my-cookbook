import RecipeForm from './RecipeForm'
import {
  act,
  findByTestId,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react'
import { mockRecipeTwo } from '../testVariables'
import userEvent from '@testing-library/user-event'

import { Provider } from 'react-redux'
import applicationStore from '../../../store'
import { renderWithProviders } from '../../../utils/testingUtils'
const store = applicationStore()

// Add three images
const file = new File(['hello'], 'testImage1.jpg', {
  type: 'image/png',
})
const file2 = new File(['hello'], 'testImage2.jpg', {
  type: 'image/png',
})
const file3 = new File(['hello'], 'testImage3.jpg', {
  type: 'image/png',
})

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
    await act(async () => await renderWithProviders(<RecipeForm />))

    // Verify Upload Image text shown
    expect(screen.getByText(/Upload An Image/i)).toBeInTheDocument()
  })

  test('Test help tooltip shows', async () => {
    await act(async () => await renderWithProviders(<RecipeForm />))

    // Shows tooltip
    const button = await screen.findByRole('button', {
      name: 'Click Image to Choose New Image',
    })
    // Tooltip displays text on hover
    await act(async () => {
      await userEvent.hover(button)
    })
    expect(await screen.findByRole('tooltip')).toBeInTheDocument()
  })

  test('Test delete tooltip shows', async () => {
    await act(async () => await renderWithProviders(<RecipeForm />))

    // Shows tooltip
    const button = await screen.findByRole('button', {
      name: 'Delete Current Image',
    })
    // Tooltip displays text on hover
    await act(async () => {
      await userEvent.hover(button)
    })
    expect(await screen.findByRole('tooltip')).toBeInTheDocument()
  })

  test('Test clear tooltip shows', async () => {
    await act(async () => await renderWithProviders(<RecipeForm />))

    // Shows tooltip
    const button = await screen.findByRole('button', {
      name: 'Delete All Images',
    })
    // Tooltip displays text on hover
    await act(async () => {
      await userEvent.hover(button)
    })
    expect(await screen.findByRole('tooltip')).toBeInTheDocument()
  })

  test('Test Images Container Loads', async () => {
    await act(async () => await renderWithProviders(<RecipeForm />))

    const fileInput = await screen.findByLabelText('Upload Image Input')

    await waitFor(async () => {
      await userEvent.upload(fileInput, file)
      await userEvent.upload(fileInput, file2)
      await userEvent.upload(fileInput, file3)
    })

    // Displays first image
    expect(await screen.findByAltText('Image 1')).toBeInTheDocument()
    expect(screen.queryByText(/Upload An Image/i)).not.toBeInTheDocument()

    // Displays pagination
    const imgPageination = await screen.findByRole('navigation', {
      name: 'pagination navigation',
    })
    expect(imgPageination).toBeInTheDocument()

    // Clicking on page 2 changes image
    const nextPageBtns = screen.getAllByRole('button', {
      name: 'Go to next page',
    })

    await userEvent.click(nextPageBtns[0])
    expect(await screen.findByRole('img')).toBeInTheDocument()
    expect(await screen.findByAltText('Image 2')).toBeInTheDocument()

    expect(screen.queryByText(/Upload An Image/i)).not.toBeInTheDocument()

    // Displays Delete Image Clicking Delete image shows different page
    expect(
      screen.getByRole('button', {
        name: 'Go to page 3',
      })
    ).toBeInTheDocument()

    const deleteButton = screen.getByRole('button', {
      name: 'Delete Current Image',
    })

    await userEvent.click(deleteButton)

    expect(
      await screen.findByRole('button', {
        name: 'page 1',
      })
    ).toBeInTheDocument()

    expect(
      screen.queryByRole('button', {
        name: 'Go to page 3',
      })
    ).not.toBeInTheDocument()

    // Displays Clear All and Clicking removes all images and shows Upload Image
    const clearButton = screen.getByRole('button', {
      name: 'Delete All Images',
    })

    expect(screen.queryByText(/Upload An Image/i)).not.toBeInTheDocument()

    await userEvent.click(clearButton)
    expect(screen.getByText(/Upload An Image/i)).toBeInTheDocument()
  })
})

describe('Make sure tabs all work', () => {})

describe('Make sure name and steps work', () => {})
