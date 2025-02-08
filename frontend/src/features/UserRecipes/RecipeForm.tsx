/*

Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com

*/

import { useParams } from 'react-router-dom'
import { useGetRecipeQuery } from '../api/apiSlice'
import React, { useState } from 'react'
import { Recipe, RecipeObject } from '../api/types'

/**
 * File name: RecipeForm.tsx
 * Task - This component allows users to generate or update user submitted recipes via a form.
 * @author Camille Jones - crjone24@gmail.com
 */

interface RecipeFormProps {}

const EditRecipe = () => {
  const { recipeId } = useParams()
  const { data: recipe, isFetching, isError } = useGetRecipeQuery(recipeId!)

  if (isFetching) {
    return <h2>Loading</h2>
  } else if (isError) {
    return <h2>Whoops! We can't find your recipe!</h2>
  } else {
    if (typeof recipe == 'undefined')
      return <h2>Whoops! We can't find your recipe!</h2>

    return recipe
  }
}

const RecipeForm = () => {
  const { isNewRecipe } = useParams()

  let userRecipe: Recipe | undefined = new RecipeObject()

  // Editing a recipe, so load in recipe data
  if (!isNewRecipe) {
    // Attempt to get the passed recipe from the database
    const recipe = EditRecipe()
    if (React.isValidElement(recipe)) return recipe

    userRecipe = recipe as Recipe
  }

  return <section className="recipe-form"></section>
}

export default RecipeForm
