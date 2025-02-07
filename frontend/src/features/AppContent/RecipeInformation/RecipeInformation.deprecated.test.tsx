/*
Copyright (C) 2022 SE CookBook
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com
*/

import React from 'react'
import { render, waitFor, fireEvent } from '@testing-library/react'
import RecipeInformation from './RecipeInformation'
import { ThemeProvider } from '../../Themes/themeContext'
import { BrowserRouter } from 'react-router-dom'
import axios from 'axios'

// Mock axios to avoid issues with the import statement
jest.mock('axios', () => ({
  get: jest.fn(),
}))

// deprecated recipe info test
describe.skip('RecipeInformationTests', () => {
  // Test migrated
  // test('shows recipe information correctly', () => {
  //   const { getByTestId } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByTestId('RecipeInfo-comp-43')).toBeInTheDocument()
  // })

  // Additional tests

  // Test migrated
  // test('renders recipe title', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Recipe Title/i)).toBeInTheDocument()
  // })

  // Test migrated
  // test('renders recipe image', () => {
  //   const { getByAltText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByAltText(/Recipe Image/i)).toBeInTheDocument()
  // })

  // Test migrated
  // test('renders ingredients section', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Ingredients/i)).toBeInTheDocument()
  // })

  // Test migrated
  // test('renders instructions section', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Instructions/i)).toBeInTheDocument()
  // })

  // Test migrated
  // test('renders share on WhatsApp button', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Share using WhatsApp/i)).toBeInTheDocument()
  // })

  // Test migrated
  // test('share button triggers WhatsApp sharing', () => {
  //   window.open = jest.fn()
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   const shareButton = getByText(/Share using WhatsApp/i)
  //   shareButton.click()
  //   expect(window.open).toHaveBeenCalledWith(
  //     expect.stringContaining('https://api.whatsapp.com/send?text='),
  //     '_blank'
  //   )
  // })

  // Test migrated - altered to finding by "Rating" text
  // test('renders rating component', () => {
  //   const { getByTestId } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByTestId('rating-comp')).toBeInTheDocument()
  // })

  // Test migrated
  // test('renders preparation time', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Preparation Time/i)).toBeInTheDocument()
  // })

  // Test migrated
  // test('renders servings information', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Servings/i)).toBeInTheDocument()
  // })

  // Not on the website
  // test('renders author information', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Author/i)).toBeInTheDocument()
  // })

  // Not on the website
  // test('renders category information', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Category/i)).toBeInTheDocument()
  // })

  // Test migrated
  // test('renders cuisine type', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Cuisine/i)).toBeInTheDocument()
  // })

  // Not on the website
  // test('renders difficulty level', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Difficulty/i)).toBeInTheDocument()
  // })

  // Not on the website
  // test('renders nutrition facts', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Nutrition Facts/i)).toBeInTheDocument()
  // })

  // Not on the website
  // test('renders cooking method', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Cooking Method/i)).toBeInTheDocument()
  // })

  // Not on the website
  // test('renders tags section', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Tags/i)).toBeInTheDocument()
  // })

  // Not on the website
  // test('renders source information', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Source/i)).toBeInTheDocument()
  // })

  // Not on the website
  // test('renders date added', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Date Added/i)).toBeInTheDocument()
  // })

  // Not on the website
  // test('renders last updated date', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Last Updated/i)).toBeInTheDocument()
  // })

  // Not on the website
  // test('renders comments section', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Comments/i)).toBeInTheDocument()
  // })

  // Not on the website
  // test('renders related recipes section', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Related Recipes/i)).toBeInTheDocument()
  // })

  // Move this to future Section
  test('renders favorite button', () => {
    const { getByTestId } = render(
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
    expect(getByTestId('favorite-button')).toBeInTheDocument()
  })

  // Move this to future Section
  test('favorite button toggles favorite state', () => {
    const { getByTestId } = render(
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
    const favoriteButton = getByTestId('favorite-button')
    expect(favoriteButton).toHaveAttribute('aria-pressed', 'false')
    favoriteButton.click()
    expect(favoriteButton).toHaveAttribute('aria-pressed', 'true')
  })

  // Not a planned feature
  // test('renders video tutorial if available', () => {
  //   const { queryByTestId } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(queryByTestId('video-tutorial')).toBeInTheDocument()
  // })

  // Not a planned feature
  // test('renders no video message if video not available', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   // Assuming the component shows this text when no video is available
  //   expect(getByText(/No video tutorial available/i)).toBeInTheDocument()
  // })

  // Not a planned feature
  // test('renders allergens information', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Allergens/i)).toBeInTheDocument()
  // })

  // Not a planned feature
  // test('renders estimated cost', () => {
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Estimated Cost/i)).toBeInTheDocument()
  // })

  //
  // test('formats bold text correctly', () => {
  //   const { container } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   const boldText = container.querySelector('strong')
  //   expect(boldText).toBeInTheDocument()
  //   expect(boldText).toHaveTextContent('Bold Text')
  // })

  // Test migrated
  // test('formats list items correctly', () => {
  //   const { container } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   const listItems = container.querySelectorAll('li')
  //   expect(listItems.length).toBe(2)
  //   expect(listItems[0]).toHaveTextContent('List Item 1')
  //   expect(listItems[1]).toHaveTextContent('List Item 2')
  // })

  // Not on the website
  // test('formats regular text correctly', () => {
  //   const { container } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   const paragraphs = container.querySelectorAll('p')
  //   expect(paragraphs.length).toBe(2) // One for bold text, one for regular text
  //   expect(paragraphs[1]).toHaveTextContent('Regular text.')
  // })

  // Test Migrated
  // Accessibility Test: Ensure all images have alt text
  // test('all images have alt text', () => {
  //   const { getAllByRole } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   const images = getAllByRole('img')
  //   images.forEach((img) => expect(img).toHaveAttribute('alt'))
  // })

  // Redesigning Responsive Tests in the future
  // Responsive Design Test: Component renders correctly on mobile
  // test('renders correctly on mobile', () => {
  //   global.innerWidth = 500 // Simulate mobile width
  //   const { getByTestId } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByTestId('RecipeInfo-comp-43')).toBeInTheDocument()
  //   global.innerWidth = 1024 // Reset to default after test
  // })

  // Not Migrated
  // Error Handling Test: Simulate a network error
  // test('displays error message on network failure', () => {
  //   jest
  //     .spyOn(global, 'fetch')
  //     .mockImplementation(() => Promise.reject(new Error('Network error')))
  //   const { getByText } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   expect(getByText(/Failed to load recipe data/i)).toBeInTheDocument()
  // })

  // Test migrated - altered to show "Loading" text since spinner was
  // purposefully removed
  // Loading State Test: Verify loading is shown
  // Deprecated: Loading spinner doesn't show on page
  // todo: change this to loading text
  //   test('shows loading spinner while fetching data', () => {
  //     const { getByTestId } = render(
  //       <BrowserRouter>
  //         <ThemeProvider>
  //           <RecipeInformation />
  //         </ThemeProvider>
  //       </BrowserRouter>
  //     )
  //     expect(getByTestId('loading-spinner')).toBeInTheDocument()
  //   })

  // Not in the website - They removed the tooltip
  // Interaction Test: Hover over an help icon
  // Deprecated: Tooltip doesn't exist as of now
  // test('shows tooltip on hover over help icon', () => {
  //   const { getByTestId } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   fireEvent.mouseOver(getByTestId('help-icon'))
  //   expect(getByTestId('tooltip')).toBeInTheDocument()
  // })

  // Test migrated
  // Performance Test: Component loads within time frame
  // todo: update test to maake sure the actual recipe loads within a set timeframe
  // test('loads within acceptable time frame', async () => {
  //   const { getByTestId } = render(
  //     <BrowserRouter>
  //       <ThemeProvider>
  //         <RecipeInformation />
  //       </ThemeProvider>
  //     </BrowserRouter>
  //   )
  //   await waitFor(
  //     () => expect(getByTestId('RecipeInfo-comp-43')).toBeInTheDocument(),
  //     { timeout: 1000 }
  //   )
  // })
})
