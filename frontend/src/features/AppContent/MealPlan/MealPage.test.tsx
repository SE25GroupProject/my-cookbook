jest.mock('axios', () => ({
  get: jest.fn(),
}))

global.HTMLCanvasElement.prototype.getContext = jest.fn()

import React from 'react'
import { render, screen, waitFor, fireEvent, act } from '@testing-library/react'
import MealPage from './MealPage'
import axios from 'axios'
import { ThemeProvider } from '../../Themes/themeContext'
import { renderWithProviders } from '../../../utils/testingUtils'
import { jsPDF } from 'jspdf'

const mockedAxios = axios as jest.Mocked<typeof axios>

// jest.mock('jspdf', () => {
//   return {
//     jsPDF: jest.fn().mockImplementation(() => ({
//       save: jest.fn(),
//       text: jest.fn(),
//     })),
//   };
// });

// jest.mock('jspdf')

describe('MealPage Component', () => {
  //   beforeEach(() => {
  //     mockedAxios.get.mockResolvedValue({
  //       data: [
  //         {
  //           day: 0,
  //           recipe: { name: 'Pasta', instructions: ['Boil water', 'Cook pasta'] },
  //         },
  //         {
  //           day: 2,
  //           recipe: {
  //             name: 'Salad',
  //             instructions: ['Chop vegetables', 'Mix dressing'],
  //           },
  //         },
  //       ],
  //     })
  //   })

  afterEach(() => {
    jest.clearAllMocks()
  })

  test('renders the component and displays the title', async () => {
    await renderWithProviders(<MealPage />)
    expect(await screen.findByText('My Meal Plan')).toBeInTheDocument()
  })

  test('displays a table with meal plan data', async () => {
    await renderWithProviders(<MealPage />)

    // Wait for data fetching to complete
    // await waitFor(() => expect(mockedAxios.get).toHaveBeenCalledTimes(1))

    // Check if table rows for fetched data are rendered
    expect(screen.getByText('Pasta')).toBeInTheDocument()
    expect(screen.getByText('Boil water, Cook pasta')).toBeInTheDocument()
    expect(screen.getByText('Salad')).toBeInTheDocument()
    expect(
      screen.getByText('Chop vegetables, Mix dressing')
    ).toBeInTheDocument()

    // Check for empty slots for days without meals
    expect(screen.getAllByText('No meal planned').length).toBe(5) // Remaining empty days
  })

  test('handles errors during data fetching gracefully', async () => {
    // mockedAxios.get.mockRejectedValueOnce(new Error('Network Error'))
    await renderWithProviders(<MealPage />)

    // Wait for error handling to complete
    // await waitFor(() => expect(mockedAxios.get).toHaveBeenCalledTimes(1))

    // Check for fallback behavior (e.g., empty table rows or logs)
    expect(screen.getAllByText('No meal planned').length).toBe(7) // All days are empty
  })

  test('triggers print functionality when Print Meal Plan is clicked', async () => {
    await renderWithProviders(<MealPage />)
    // let printSpy = jest.spyOn(jsPDF.API, 'save').mockImplementation()

    fireEvent.click(await screen.findByText('Print Meal Plan'))

    // expect(printSpy).toHaveBeenCalled()
  })
})
