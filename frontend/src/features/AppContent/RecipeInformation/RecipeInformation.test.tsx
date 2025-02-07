import {
  act,
  fireEvent,
  getByPlaceholderText,
  render,
  screen,
  waitFor,
} from '@testing-library/react'
import axios from 'axios'
import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider } from '../../Themes/themeContext'
import * as ACTION_TYPES from './getRecipeInformation.actionTypes'

jest.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

const getRecipeInfoInitiatorMock = () => {
  return {
    type: ACTION_TYPES.LOADING_GET_RECIPE_INFORMATION,
    payload: 'http://localhost:8000/recipe/20919',
  }
}

const getRecipeInfoSuccessMock = (data: any) => {
  return {
    type: ACTION_TYPES.SUCCESS_GET_RECIPE_INFORMATION,
    payload: data,
  }
}

const getRecipeInfoFailureMock = (error: any) => {
  return {
    type: ACTION_TYPES.FAILURE_GET_RECIPE_INFORMATION,
    payload: error,
  }
}

jest.mock('./getRecipeInformation.action.ts', () => ({
  getRecipeInfoInitiator: getRecipeInfoInitiatorMock,
  getRecipeInfoSuccess: getRecipeInfoSuccessMock,
  getRecipeInfoFailure: getRecipeInfoFailureMock,
}))

import RecipeInformation from './RecipeInformation'

describe('Recipe Display Tests', () => {
  test('Show Recipe Loading', () => {
    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )

    const recipeInfo = screen.queryByTestId('RecipeInfo')
    expect(screen.getByTestId('RecipeInfoLoading')).toBeInTheDocument()
    expect(recipeInfo).not.toBeInTheDocument()
  })

  test('Recipe Rendered in appropriate timeframe', async () => {
    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )

    await waitFor(
      () => {
        const recipeInfoLoader = screen.queryByTestId('RecipeInfoLoading')

        expect(recipeInfoLoader).not.toBeInTheDocument()
        expect(screen.getByTestId('RecipeInfo')).toBeInTheDocument()
      },
      { timeout: 1000 }
    )
  })

  test('Recipe Name is being displayed', async () => {
    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )

    expect(await screen.findByRole('heading', { level: 4 })).toBeInTheDocument()
  })

  test('Recipe image is being displayed', async () => {
    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )
    expect(await screen.findByRole('img')).toBeInTheDocument()
  })

  test('Recipe ingredients section is being displayed', async () => {
    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )
    expect(await screen.findByText(/Ingredients/i)).toBeInTheDocument()
  })

  test('Recipe instructions section is being displayed', async () => {
    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )
    expect(await screen.findByText(/Instructions/i)).toBeInTheDocument()
  })

  test('Sharing buttons are being displayed', async () => {
    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )
    expect(await screen.findByText(/WhatsApp/i)).toBeInTheDocument()
    expect(await screen.findByText(/Slack/i)).toBeInTheDocument()
    expect(await screen.findByText(/Discord/i)).toBeInTheDocument()
  })

  test('WhatsApp button triggers Whatsapp sharing', async () => {
    window.open = jest.fn()

    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )

    const shareButton = await screen.findByText(/WhatsApp/i)
    shareButton.click()
    expect(window.open).toHaveBeenCalledWith(
      expect.stringContaining('https://api.whatsapp.com/send?text='),
      '_blank'
    )
  })

  test('Discord button triggers Discord sharing', async () => {
    window.open = jest.fn()

    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )
    // Expect the modal to be closed
    var copyModal = screen.queryByTestId('CopyModal')
    expect(copyModal).not.toBeInTheDocument()

    // Open the modal
    const shareButton = await screen.findByText(/Discord/i)
    act(() => {
      shareButton.click()
    })

    // Expect the modal to open
    expect(await screen.findByTestId('CopyModal')).toBeInTheDocument()

    // Click the copy button
    const copyButton = await screen.findByRole('button', { name: /Copy/i })
    act(() => {
      copyButton.click()
    })

    // Expect the modal to be closed again
    var copyModal = screen.queryByTestId('CopyModal')
    expect(copyModal).not.toBeInTheDocument()

    // expect it to beshared
    expect(window.open).toHaveBeenCalledWith(
      expect.stringContaining('https://discord.com/channels/@me?message='),
      '_blank'
    )
  })

  test('Slac button triggers Slack sharing', async () => {
    window.open = jest.fn()

    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )
    // Expect the modal to be closed
    var copyModal = screen.queryByTestId('CopyModal')
    expect(copyModal).not.toBeInTheDocument()

    // Open the modal
    const shareButton = await screen.findByText(/Slack/i)
    act(() => {
      shareButton.click()
    })

    // Expect the modal to open
    expect(await screen.findByTestId('CopyModal')).toBeInTheDocument()

    // Click the copy button
    const copyButton = await screen.findByRole('button', { name: /Copy/i })
    act(() => {
      copyButton.click()
    })

    // Expect the modal to be closed again
    var copyModal = screen.queryByTestId('CopyModal')
    expect(copyModal).not.toBeInTheDocument()

    // expect it to beshared
    expect(window.open).toHaveBeenCalledWith(
      expect.stringContaining('https://slack.com/intl/en-us/share?text='),
      '_blank'
    )
  })

  test('Recipe Rating section is being displayed', async () => {
    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )
    expect(await screen.findByText(/Rating/i)).toBeInTheDocument()
  })

  test('Recipe Prep Time section is being displayed', async () => {
    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )
    expect(await screen.findByText(/Prep Time/i)).toBeInTheDocument()
  })

  test('Recipe Servings section is being displayed', async () => {
    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )
    expect(await screen.findByText(/Servings/i)).toBeInTheDocument()
  })

  test('Recipe Cuisine section is being displayed', async () => {
    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )
    expect(await screen.findByText(/Cuisine/i)).toBeInTheDocument()
  })
})

describe('Text Formatting', () => {
  test('formats text correctly', async () => {
    mockedAxios.post.mockResolvedValue({
      data: {
        response:
          'this is **bold**. \n* This is an item\n* This is a second\n ',
      },
    })
    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )
    // Hit customize Button
    const customizeBtn = await screen.findByText('CUSTOMIZE')

    act(() => {
      customizeBtn.click()
    })

    // Query AI
    const aiInput = await screen.findByPlaceholderText(
      'Type your customization...'
    )

    act(() => {
      fireEvent.change(aiInput, {
        target: { value: 'test value' },
      })
      const aiSubmit = screen.getByTestId('ai-submit')
      aiSubmit.click()
    })

    const strongText = await screen.findByRole('strong')

    expect(strongText).toBeInTheDocument()
    expect(strongText).toHaveTextContent('bold')

    const listItems = await screen.findAllByRole('listitem')

    expect(listItems).toHaveLength(2)
  })

  test('all images have alt text', async () => {
    render(
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )

    const images = await screen.findAllByRole('img')
    images.forEach((img) => expect(img).toHaveAttribute('alt'))
  })
})
