import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { Recipe, RecipeObject } from './types'

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: 'http://localhost:8000',
    // credentials: 'same-origin',
    mode: 'cors',

    prepareHeaders: (headers) => {
      //   const accessToken = localStorage.getItem('token')
      //   if (accessToken) {
      //     headers.set('authorization', `Bearer ${accessToken}`)
      //     headers.set('Content-Type', 'application/json')
      //   }
      headers.set('Access-Control-Allow-Origin', '*')

      return headers
    },
  }),
  tagTypes: ['Recipe', 'Post', 'ShoppingList', 'MealPlan'],
  endpoints: (builder) => ({
    getRecipes: builder.query<Recipe[], void>({
      query: () => '/recipes',
      providesTags: (result = [], error, arg) => [
        'Recipe',
        { type: 'Recipe', id: 'LIST' },
        ...result.map(
          ({ recipeId }) => ({ type: 'Recipe', recipeId }) as const
        ),
      ],
    }),
    // Get Recipe will return a Recipe, but takes a string
    getRecipe: builder.query<Recipe, string>({
      query: (recipeId) => `/recipe/${recipeId}`,
      providesTags: (result, error, arg) => [{ type: 'Recipe', id: arg }],
    }),
    addNewRecipe: builder.mutation<Recipe, Recipe>({
      query: (initialRecipe) => ({
        url: '/recipe',
        method: 'POST',
        body: initialRecipe,
      }),
      invalidatesTags: [{ type: 'Recipe', id: 'LIST' }],
    }),
    editRecipe: builder.mutation<Recipe, Recipe>({
      query: (recipe) => ({
        url: `/recipe/${recipe.recipeId}`,
        method: 'PATCH',
        body: recipe,
      }),
      invalidatesTags: (result, error, arg) => [
        { type: 'Recipe', id: arg.recipeId },
      ],
    }),
  }),
})

export const {
  useGetRecipesQuery,
  useGetRecipeQuery,
  useAddNewRecipeMutation,
  useEditRecipeMutation,
} = apiSlice
