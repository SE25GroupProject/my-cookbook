/*

Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com

*/

import React, { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import StarIcon from '@mui/icons-material/Star'
import {
  Typography,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CardActionArea,
  Pagination,
  CircularProgress,
  SelectChangeEvent,
  Box,
  FormHelperText,
} from '@mui/material'
import './RecipeList.css'
import { RECIPE_CATEGORIES, RECIPE_COOKTIME } from './recipeCategories'
import { useTheme } from '../../Themes/themeContext'
import {
  NutritionMax,
  Recipe,
  RecipeListData,
  RecipeListIngredientsRequest,
  RecipeListNutritionRequest,
  RecipeListResponse,
} from '../../api/types'
import {
  useGetCountIngredientsMutation,
  useGetCountNutritionMutation,
  useGetRecipeListByIngredientsMutation,
  useGetRecipeListByNutritionMutation,
} from './RecipeListSlice'
import { SearchBarProps } from '../AppContent'
import RecipeListItem from './RecipeLIstItem'
/**
 * File name: RecipeList.tsx
 * Task - This component displays a list of recipes based on the ingredients inputed.
 * This component is a dynamic component and is seen only when you click on a recipe from the recipe list.
 */

interface RecipeListProps {
  ingredients: String[] | null
  nutrition: NutritionMax | null
}

const RecipeList = ({ toggleSearchBar }: SearchBarProps) => {
  const { theme } = useTheme()
  const { state } = useLocation()

  const [recipeList, setRecipeList] = useState<RecipeListData[]>([])
  const [filtedRecipeList, setFilteredRecipeList] = useState<RecipeListData[]>(
    []
  )
  const [page, setPage] = useState<number>(1)
  const [totalCount, setTotalCount] = useState<number>(0)
  // const [loading, setLoading] = useState<boolean>(false)
  const [selectedCategory, setSelectedCategory] = useState<string>('')
  const [selectedCookTime, setSelectedCookTime] = useState<string>('')
  const [hidden, setHidden] = useState<boolean>(false)

  const [getListByIngredients, { isLoading: ingredientsLoading }] =
    useGetRecipeListByIngredientsMutation()
  const [getListByNutrition, { isLoading: nutritionLoading }] =
    useGetRecipeListByNutritionMutation()

  const [getCountIngredients, { isLoading: ingCountLoading }] =
    useGetCountIngredientsMutation()
  const [getCountNutrition, { isLoading: nutrCountLoading }] =
    useGetCountNutritionMutation()

  useEffect(() => {
    if (state?.ingredients) {
      let request: RecipeListIngredientsRequest = {
        ingredients: state.ingredients,
        page: page,
      }
      getCountIngredients(request)
        .unwrap()
        .then((response: number) => {
          setTotalCount(response)
        })
        .catch((err) => console.log(err))
    } else if (state?.nutrition) {
      let request: RecipeListNutritionRequest = {
        caloriesMax: state.nutrition.caloriesMax,
        fatMax: state.nutrition.fatMax,
        sugMax: state.nutrition.sugMax,
        proMax: state.nutrition.proMax,
        page: page,
      }
      getCountNutrition(request)
        .unwrap()
        .then((response: number) => {
          setTotalCount(response)
        })
        .catch((err) => console.log(err))
    }
  }, [])

  useEffect(() => {
    toggleSearchBar(false)
  }, [recipeList])

  function convertToMinutes(timeString: string) {
    timeString = timeString.replace(/\s+/g, '').replace('<', '')
    const match = timeString.match(/(\d+)H(?:\s*(\d+)M)?|(\d+)M/)
    if (match) {
      const hours = match[1] ? parseInt(match[1], 10) : 0
      const minutes = match[2]
        ? parseInt(match[2], 10)
        : match[3]
          ? parseInt(match[3], 10)
          : 0
      return hours * 60 + minutes
    } else {
      return 0
    }
  }

  function unwrapResponse(response: RecipeListResponse) {
    setRecipeList(response.recipes)
    setTotalCount(response.count)
  }

  function RequestList() {
    console.log(state)
    if (state?.ingredients) {
      let request: RecipeListIngredientsRequest = {
        ingredients: state.ingredients,
        page: page,
      }
      getListByIngredients(request)
        .unwrap()
        .then((response: RecipeListResponse) => {
          unwrapResponse(response)
        })
        .catch((err) => console.log(err))
    }

    if (state?.nutrition) {
      let request: RecipeListNutritionRequest = {
        caloriesMax: state.nutrition.caloriesMax,
        fatMax: state.nutrition.fatMax,
        sugMax: state.nutrition.sugMax,
        proMax: state.nutrition.proMax,
        page: page,
      }
      getListByNutrition(request)
        .unwrap()
        .then((response: RecipeListResponse) => {
          unwrapResponse(response)
        })
        .catch((err) => console.log(err))
    }
  }

  useEffect(() => {
    RequestList()
  }, [state])

  useEffect(() => {
    if (selectedCategory) {
      let filtered = recipeList.filter(
        (recipe) => recipe.category === selectedCategory
      )
      setFilteredRecipeList(filtered)

      if (selectedCookTime) {
        setHidden(true)
        const comp = convertToMinutes(selectedCookTime)
        let f1 = filtered.filter(
          (recipe) => convertToMinutes(recipe.cookTime) < comp
        )
        if (f1.length === 0) {
          setHidden(false)
        } else {
          filtered = f1
        }
      }

      setFilteredRecipeList(filtered)
    } else {
      setFilteredRecipeList(recipeList)
    }
  }, [selectedCategory, selectedCookTime, recipeList])

  const handlePageChange = (
    event: React.ChangeEvent<unknown>,
    value: number
  ) => {
    setPage(value)

    RequestList()

    setSelectedCategory('')
  }

  // Handle category change
  const handleCategoryChange = (event: SelectChangeEvent<string>) => {
    setSelectedCategory(event.target.value)
  }

  const handleCookTimeChange = (event: SelectChangeEvent<string>) => {
    setSelectedCookTime(event.target.value)
  }

  return (
    <>
      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          alignItems: 'center',
          gap: 2,
          mb: 2,
          m: 2,
          backgroundColor: theme.headerColor, // Theme background
          color: theme.color, // Theme color
        }}
      >
        <Box />
        <Pagination
          page={page}
          count={Math.ceil(totalCount / 10)}
          onChange={handlePageChange}
          color="secondary"
          variant="outlined"
          shape="rounded"
          sx={{
            display: 'flex',
            alignItems: 'center',
            height: '100%',
            color: theme.background,
          }}
        />
        {totalCount > 0 && (
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'space-between', // Ensures space between both components
              alignItems: 'center', // Vertically aligns the components in the middle
              width: '100%', // Ensures the Box takes the full width
            }}
          >
            {/* Category FormControl */}
            <FormControl
              sx={{
                display: 'flex',
                justifyContent: 'flex-end',
                color: theme.color,
                backgroundColor: theme.headerColor,
                marginTop: '15px',
                marginBottom: '10px',
                width: '48%', // Adjust width to fit both components in the same row
              }}
              size="small"
            >
              <InputLabel
                sx={{
                  color: theme.color,
                  fontSize: '18px',
                  '&.Mui-focused': {
                    color: theme.color,
                  },
                }}
              >
                Category
              </InputLabel>
              <Select
                value={selectedCategory}
                onChange={handleCategoryChange}
                label="Category"
                sx={{
                  color: theme.color,
                  fontSize: '15px',
                  marginTop: '3px',
                  height: '30px',
                  width: '100%',
                  '.MuiSelect-icon': {
                    color: theme.color,
                    backgroundColor: theme.headerColor,
                  },
                  '&:hover .MuiOutlinedInput-notchedOutline': {
                    borderColor: theme.color,
                  },
                  '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                    borderColor: theme.color,
                  },
                }}
                MenuProps={{
                  PaperProps: {
                    sx: {
                      maxHeight: 200,
                      overflowY: 'auto',
                      marginTop: '8px',
                      backgroundColor: theme.background,
                      color: theme.color,
                    },
                  },
                }}
              >
                <MenuItem value="">All Categories</MenuItem>
                {RECIPE_CATEGORIES.map((category, index) => (
                  <MenuItem
                    key={index}
                    value={category}
                    sx={{
                      backgroundColor: theme.background,
                      color: theme.color,
                      '&:hover': {
                        backgroundColor: theme.headerColor,
                        color: theme.color,
                      },
                    }}
                  >
                    {category}
                  </MenuItem>
                ))}
              </Select>
              {selectedCategory && filtedRecipeList.length === 0 && (
                <FormHelperText sx={{ color: '#f44336', marginTop: '8px' }}>
                  No recipes found in this category.
                </FormHelperText>
              )}
            </FormControl>

            {/* Cook Time FormControl */}
            {selectedCategory != '' && filtedRecipeList.length > 0 && (
              <FormControl
                sx={{
                  display: 'flex',
                  justifyContent: 'flex-end',
                  color: theme.color,
                  backgroundColor: theme.headerColor,
                  marginTop: '15px',
                  marginBottom: '10px',
                  width: '48%', // Adjust width to fit both components in the same row
                }}
                size="small"
              >
                <InputLabel
                  sx={{
                    color: theme.color,
                    fontSize: '18px',
                    '&.Mui-focused': {
                      color: theme.color,
                    },
                  }}
                >
                  Cook Time
                </InputLabel>
                <Select
                  value={selectedCookTime}
                  onChange={handleCookTimeChange}
                  label="Cook Time"
                  sx={{
                    color: theme.color,
                    fontSize: '15px',
                    marginTop: '3px',
                    height: '30px',
                    width: '100%',
                    '.MuiSelect-icon': {
                      color: theme.color,
                      backgroundColor: theme.headerColor,
                    },
                    '&:hover .MuiOutlinedInput-notchedOutline': {
                      borderColor: theme.color,
                    },
                    '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                      borderColor: theme.color,
                    },
                  }}
                  MenuProps={{
                    PaperProps: {
                      sx: {
                        maxHeight: 200,
                        overflowY: 'auto',
                        marginTop: '8px',
                        backgroundColor: theme.background,
                        color: theme.color,
                      },
                    },
                  }}
                >
                  <MenuItem value="">All Categories</MenuItem>
                  {RECIPE_COOKTIME.map((time, index) => (
                    <MenuItem
                      key={index}
                      value={time}
                      sx={{
                        backgroundColor: theme.background,
                        color: theme.color,
                        '&:hover': {
                          backgroundColor: theme.headerColor,
                          color: theme.color,
                        },
                      }}
                    >
                      {time}
                    </MenuItem>
                  ))}
                </Select>
                {selectedCookTime && !hidden && (
                  <FormHelperText sx={{ color: '#f44336', marginTop: '8px' }}>
                    No recipes found in selected cooktime.
                  </FormHelperText>
                )}
              </FormControl>
            )}
          </Box>
        )}
      </Box>
      {!(ingredientsLoading || nutritionLoading) ? (
        totalCount > 0 ? (
          (selectedCategory && filtedRecipeList.length > 0
            ? filtedRecipeList
            : recipeList
          ).map((recipe: RecipeListData, index: number) => {
            return <RecipeListItem recipe={recipe} index={index} />
          })
        ) : !(ingCountLoading || nutrCountLoading) ? (
          <Typography
            variant="h5"
            component="div"
            sx={{ m: 4, color: theme.color }} // Theme color for no recipes found
            className="no-recipe-found"
          >
            Currently our database does not have any recipes with the selected
            ingredients. Check back in later for any updates.
          </Typography>
        ) : (
          <CircularProgress
            style={{ color: theme.color, margin: '50px' }} // Theme color for loader
          />
        )
      ) : (
        <CircularProgress
          style={{ color: theme.color, margin: '50px' }} // Theme color for loader
        />
      )}
      <Pagination
        page={page}
        count={Math.ceil(totalCount / 10)}
        sx={{
          m: 2,
          backgroundColor: theme.headerColor,
          color: theme.color, // Theme color for pagination
        }}
        onChange={handlePageChange}
        color="secondary"
        variant="outlined"
        shape="rounded"
      />
    </>
  )
}

export default RecipeList
