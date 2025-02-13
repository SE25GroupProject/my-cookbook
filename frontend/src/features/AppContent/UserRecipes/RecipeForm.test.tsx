import RecipeForm from './RecipeForm'
import {
  act,
  findByRole,
  findByTestId,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
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

describe('Make sure tabs all work', () => {
  test('Test Desc Tab', async () => {
    await renderWithProviders(<RecipeForm />)

    expect(
      await screen.findByRole('combobox', { name: 'Category' })
    ).toBeInTheDocument()

    expect(screen.getByRole('textbox', { name: 'Description' }))
  })
  test('Test Info Tab', async () => {
    await renderWithProviders(<RecipeForm />)

    const infoTab = await screen.findByRole('tab', { name: /info/i })
    await userEvent.click(infoTab)

    expect(screen.getByRole('spinbutton', { name: 'Servings' }))
    expect(screen.getByRole('spinbutton', { name: 'Prep Hours' }))
    expect(screen.getByRole('spinbutton', { name: 'Prep Mins' }))
    expect(screen.getByRole('spinbutton', { name: 'Cook Hours' }))
    expect(screen.getByRole('spinbutton', { name: 'Cook Mins' }))

    expect(screen.getByText(/Total:/))
  })

  test('Test Ing Tab', async () => {
    await renderWithProviders(<RecipeForm />)

    const ingTab = await screen.findByRole('tab', { name: /ing./i })
    await userEvent.click(ingTab)

    const ingInput = await screen.findByLabelText('Add Ingredient Input')
    const ingAddBtn = screen.getByRole('button', { name: 'Add New Ingredient' })
    expect(ingInput).toBeInTheDocument()
    expect(ingAddBtn)

    await userEvent.type(ingInput, 'test 1')
    await userEvent.click(ingAddBtn)

    await userEvent.type(ingInput, 'test 2')
    await userEvent.click(ingAddBtn)

    await userEvent.type(ingInput, 'test 3')
    await userEvent.click(ingAddBtn)

    await userEvent.type(ingInput, 'test 4')
    await userEvent.click(ingAddBtn)

    expect(await screen.findByText('test 1')).toBeInTheDocument()
    expect(await screen.findByText('test 2')).toBeInTheDocument()
    expect(await screen.findByText('test 3')).toBeInTheDocument()
    expect(screen.queryByText('test 4')).not.toBeInTheDocument()

    const nextPageBtns = screen.getAllByRole('button', {
      name: 'Go to next page',
    })
    await userEvent.click(nextPageBtns[0])

    expect(screen.queryByText('test 3')).not.toBeInTheDocument()
    const ingBox = await screen.findByText('test 4')
    expect(ingBox).toBeInTheDocument()

    const ingBoxInner = within(await screen.findByLabelText('Ingredient 3'))

    const ingDelete = await ingBoxInner.findByRole('button')
    await userEvent.click(ingDelete)

    expect(await screen.findByText('test 1')).toBeInTheDocument()
    expect(await screen.findByText('test 2')).toBeInTheDocument()
    expect(await screen.findByText('test 3')).toBeInTheDocument()
    expect(screen.queryByText('test 4')).not.toBeInTheDocument()
  })

  test('Test Nutr Tab', async () => {
    await renderWithProviders(<RecipeForm />)

    const nutrTab = await screen.findByRole('tab', { name: /nutr./i })
    await userEvent.click(nutrTab)

    expect(screen.getByRole('spinbutton', { name: 'Calories' }))
    expect(screen.getByRole('spinbutton', { name: 'Protein' }))
    expect(screen.getByRole('spinbutton', { name: 'Sugar' }))
    expect(screen.getByRole('spinbutton', { name: 'Fiber' }))
    expect(screen.getByRole('spinbutton', { name: 'Carbs' }))
    expect(screen.getByRole('spinbutton', { name: 'Fat' }))
    expect(screen.getByRole('spinbutton', { name: 'Saturated Fat' }))
    expect(screen.getByRole('spinbutton', { name: 'Sodium' }))
    expect(screen.getByRole('spinbutton', { name: 'Cholesterol' }))
  })
})

describe('Make sure name and steps display', () => {
  test('Test Name', async () => {
    await renderWithProviders(<RecipeForm />)

    expect(await screen.findByRole('textbox', { name: 'Name' }))
    expect(screen.getByText('Steps'))
  })
  test('Test Steps (Adding. Editing and Deleting)', async () => {
    await renderWithProviders(<RecipeForm />)
    const addStep = screen.getByRole('button', { name: 'Add New Step' })
    expect(addStep)

    expect(screen.queryByText('Test Step')).not.toBeInTheDocument()

    // Click Add Step
    await userEvent.click(addStep)

    // Input text for new step
    const addStepModal = within(await screen.findByRole('presentation'))
    const addStepInput = addStepModal.getByRole('textbox', {
      name: 'Add a Step',
    })

    expect(addStepInput).toBeInTheDocument()
    await userEvent.type(addStepInput, 'Test Step')

    // Submit new step

    const addStepButton = addStepModal.getByRole('button')
    await userEvent.click(addStepButton)

    expect(screen.queryByRole('presentation')).not.toBeInTheDocument()

    // Assert that new step appears
    expect(await screen.findByText('Test Step')).toBeInTheDocument()

    // Assert edit and delete buttons appear
    const editBtn = screen.getByRole('button', { name: /Edit Step/ })
    const deleteBtn = screen.getByRole('button', { name: /Delete Step/ })
    expect(editBtn).toBeInTheDocument()
    expect(deleteBtn)

    expect(screen.queryAllByRole('presentation')).toHaveLength(0)

    // Assert edit modal appears
    await userEvent.click(editBtn)

    const editStepModal = within(
      (await screen.findAllByRole('presentation', { hidden: false }))[1]
    )
    expect(
      editStepModal.getByRole('heading', { name: 'Edit a Step' })
    ).toBeInTheDocument()
    const saveEditBtn = editStepModal.getByRole('button', { name: 'Save Step' })
    expect(saveEditBtn).toBeInTheDocument()

    // Change step text and submit

    const editStepInput = editStepModal.getByRole('textbox')
    await userEvent.type(editStepInput, 'edited step')

    await userEvent.click(saveEditBtn)

    // assert step has been edited

    expect(await screen.findByText(/edited step/)).toBeInTheDocument()

    // Delete step and assert gone
    await userEvent.click(deleteBtn)
    expect(screen.queryByText(/edited step/)).not.toBeInTheDocument()
  })
})
