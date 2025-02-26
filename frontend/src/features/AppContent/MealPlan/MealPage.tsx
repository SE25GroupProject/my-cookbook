import React, { useState, useEffect } from 'react'
import '../HomePage/HomePage.css'
import { useTheme } from '../../Themes/themeContext'
import axios from 'axios'
import {
  useGetMealPlanQuery,
  useRemoveFromMealPlanMutation,
} from './MealPlanSlice'
import { useAuth } from '../Authentication/AuthProvider'
import { PostRecipe } from '../../api/types'
import {
  Backdrop,
  Button,
  CircularProgress,
  IconButton,
  Link,
  Typography,
} from '@mui/material'
import jsPDF from 'jspdf'
import { Delete, Dock } from '@mui/icons-material'
import autoTable from 'jspdf-autotable'
import { useNavigate } from 'react-router-dom'
import { useLazyGetBatchRecipesQuery } from '../../api/apiSlice'
import { doc } from 'prettier'

const MealPage = () => {
  const { theme } = useTheme()
  const auth = useAuth()
  const navigateTo = useNavigate()

  const [mealPlan, setMealPlan] = useState<Record<number, PostRecipe>>({}) // One meal per day
  const daysOfTheWeek = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday',
  ]

  const userId = auth?.user.id ?? -1
  const { data: mealPlanEntries } = useGetMealPlanQuery(userId, {
    skip: userId == -1,
  })
  const [removeFromMealPlan, result] = useRemoveFromMealPlanMutation()

  useEffect(() => {
    let allEntries = {}
    if (mealPlanEntries) {
      allEntries = {
        ...Object.fromEntries(
          mealPlanEntries?.map((entry) => [entry.day, entry.recipe])
        ),
      }
    }

    setMealPlan(allEntries)
  }, [mealPlanEntries])

  const navigateRecipe = (recipeId: number) => {
    navigateTo('/recipe-details/' + recipeId)
  }

  const handleRemove = (day: number) => {
    if (!auth) return
    removeFromMealPlan({ day: day, userId: auth?.user.id })
  }

  const [getMealRecipes] = useLazyGetBatchRecipesQuery()

  const printMealPlan = () => {
    const recipeIds =
      mealPlanEntries?.map((entry) => entry.recipe.recipeId) ?? []

    getMealRecipes(recipeIds)
      .unwrap()
      .then((response) => {
        // Batch call to get all the recipes and promise?

        const pdf = new jsPDF({ format: 'letter' })
        pdf.setFontSize(48)
        pdf.text('Your Custom Meal Plan', 11, 20)

        pdf.setFontSize(24)
        pdf.text('We hope you enjoy!', 13, 30)

        const headers = ['Day', 'Recipe']

        const body = daysOfTheWeek.map((day, index) => [
          day,
          mealPlan[index]?.name ?? 'No Meal Planned',
        ])

        autoTable(pdf, {
          head: [headers],
          body: body,
          startY: 40,
          headStyles: {
            fillColor: theme.background,
            textColor: theme.color,
            fontStyle: 'bold',
            fontSize: 14,
            halign: 'left',
          },
          columnStyles: {
            0: { cellWidth: 40 },
            1: { cellWidth: 150 },
          },
          alternateRowStyles: { fillColor: [255, 245, 217] },
          bodyStyles: {
            fontSize: 10,
            cellPadding: { top: 1, right: 5, bottom: 1, left: 2 },
            textColor: [0, 0, 0],
          },
          margin: { top: 10, left: 13 },
        })

        response?.forEach((recipe, index) => {
          pdf.addPage('letter')

          pdf.setFontSize(48)
          pdf.text(recipe.name, 11, 20)

          if (recipe.images[0]) {
            var img = new Image()
            img.src = recipe.images[0]
            pdf.addImage(img, 'png', 100, 10, 124, 70)
          }
          pdf.setFontSize(10)
          pdf.text(`Prep Time: ${recipe.prepTime}`, 131, 55)
          pdf.text(`Cook Time: ${recipe.cookTime}`, 161, 55)
          pdf.text(`Total Time: ${recipe.totalTime}`, 131, 60)
          pdf.text(`Category: ${recipe.category}`, 161, 60)

          pdf.setFontSize(18)
          pdf.text(`Calories: ${recipe.calories}`, 11, 43)
          pdf.text(`Servings: ${recipe.servings}`, 160, 43)

          pdf.setFontSize(10)
          pdf.text(`Fat: ${recipe.fat}`, 11, 55)
          pdf.text(`Carbs: ${recipe.carbs}`, 41, 55)
          pdf.text(`Fiber: ${recipe.fiber}`, 71, 55)
          pdf.text(`Saturated Fat: ${recipe.saturatedFat}`, 101, 55)

          pdf.text(`Sugar: ${recipe.sugar}`, 11, 60)
          pdf.text(`Protein: ${recipe.protein}`, 41, 60)
          pdf.text(`Cholesterol: ${recipe.cholesterol}`, 71, 60)
          pdf.text(`Sodium: ${recipe.sodium}`, 101, 60)

          pdf.setFontSize(14)
          pdf.text(`Description:`, 11, 78)
          pdf.text(`Ingredients:`, 160, 78)

          pdf.setFontSize(10)
          var splitDescription = pdf.splitTextToSize(recipe.description, 120)
          pdf.text(splitDescription, 11, 85)

          pdf.text(recipe.ingredients, 160, 85)

          const recipeBody = recipe.instructions.map((istr, istrIndex) => [
            istr.step,
            istr.instruction,
          ])

          autoTable(pdf, {
            head: [['Step', 'Instruction']],
            body: recipeBody,
            startY: 150,
            headStyles: {
              fillColor: theme.background,
              textColor: theme.color,
              fontStyle: 'bold',
              fontSize: 14,
              halign: 'left',
            },
            columnStyles: {
              0: { cellWidth: 15 },
              1: { cellWidth: 175 },
            },
            alternateRowStyles: { fillColor: [255, 245, 217] },
            bodyStyles: {
              fontSize: 10,
              cellPadding: { top: 1, right: 5, bottom: 1, left: 2 },
              textColor: [0, 0, 0],
            },
            margin: { top: 10, left: 13 },
          })
        })

        pdf.save('MealPlan.pdf')
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return (
    <div
      style={{
        backgroundColor: theme.background,
        color: theme.color,
        padding: '20px',
      }}
    >
      <h2>My Meal Plan</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid', padding: '8px' }}>Day</th>
            <th style={{ border: '1px solid', padding: '8px' }}>Recipe</th>
            <th style={{ border: '1px solid', padding: '8px' }}>Action</th>
          </tr>
        </thead>
        <tbody>
          {daysOfTheWeek.map((day, index) => (
            <tr key={index}>
              <td style={{ border: '1px solid', padding: '8px' }}>{day}</td>
              <td style={{ border: '1px solid', padding: '8px' }}>
                {mealPlan[index]?.name ? (
                  <Button
                    variant="text"
                    onClick={(e) => navigateRecipe(mealPlan[index].recipeId)}
                  >
                    <Typography variant="h5">
                      {mealPlan[index]?.name}
                    </Typography>
                  </Button>
                ) : (
                  'No meal planned'
                )}
              </td>
              <td style={{ border: '1px solid', padding: '8px' }}>
                {mealPlan[index] && (
                  <IconButton
                    onClick={(e) => mealPlan[index] && handleRemove(index)}
                  >
                    <Delete color="error" />
                  </IconButton>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button
        onClick={printMealPlan}
        style={{
          backgroundColor: theme.headerColor,
          color: theme.color,
          marginRight: '10px',
          transition: 'transform 0.2s ease, background-color 0.2s ease',
          marginTop: '20px',
          padding: '10px 20px',
        }}
        onMouseEnter={(e) =>
          (e.currentTarget.style.backgroundColor = theme.background)
        }
        onMouseLeave={(e) =>
          (e.currentTarget.style.backgroundColor = theme.headerColor)
        }
      >
        Print Meal Plan
      </button>

      {result.isLoading && (
        <Backdrop
          sx={(bdTheme) => ({
            color: '#fff',
            zIndex: bdTheme.zIndex.drawer + 1,
          })}
          open={true}
        >
          <CircularProgress color="inherit" />
        </Backdrop>
      )}
    </div>
  )
}

export default MealPage
