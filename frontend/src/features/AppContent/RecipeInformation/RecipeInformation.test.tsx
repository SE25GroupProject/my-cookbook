import { getByTestId, render, screen, waitFor } from '@testing-library/react'
import axios from 'axios'
import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider } from '../../Themes/themeContext'
import * as ACTION_TYPES from './getRecipeInformation.actionTypes'

jest.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

const yourActionMock = jest.fn()

const getRecipeInfoInitiatorMock = () => {
  return {
    type: ACTION_TYPES.LOADING_GET_RECIPE_INFORMATION,
    payload: 'http://localhost:8000/recipe/12069',
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
  test('Recipe Name is being displayed', async () => {
    //   const recipe = [{ name: 'Bob' }]
    //   const resp = { data: recipe }
    //   mockedAxios.get.mockResolvedValue(resp)
    console.log('test')
    render(
      <BrowserRouter>
        <ThemeProvider>
          <RecipeInformation />
        </ThemeProvider>
      </BrowserRouter>
    )
    await waitFor(
      () =>
        expect(screen.getByRole('heading', { level: 4 })).toBeInTheDocument(),
      { timeout: 2000 }
    )
  })
})
