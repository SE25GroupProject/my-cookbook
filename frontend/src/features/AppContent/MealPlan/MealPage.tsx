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
import { Button, IconButton, Link, Typography } from '@mui/material'
import jsPDF from 'jspdf'
import { Delete, Dock } from '@mui/icons-material'
import autoTable from 'jspdf-autotable'
import { useNavigate } from 'react-router-dom'

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
  const [removeFromMealPlan] = useRemoveFromMealPlanMutation()

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

  const printMealPlan = () => {
    const recipeIds = mealPlanEntries?.map((entry) => entry.recipe.recipeId)

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

    mealPlanEntries?.forEach((entry, index) => {
      pdf.addPage('letter')

      pdf.setFontSize(48)
      pdf.text(entry.recipe.name, 11, 20)
    })

    pdf.save('MealPlan.pdf')
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
    </div>
  )
}

export default MealPage
