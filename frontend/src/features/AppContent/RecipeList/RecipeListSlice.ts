import { apiSlice } from '../../api/apiSlice'
import {
  RecipeListIngredientsRequest,
  RecipeListNutritionRequest,
  RecipeListResponse,
} from '../../api/types'

export const RecipeListSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getRecipeListByIngredients: builder.mutation<
      RecipeListResponse,
      RecipeListIngredientsRequest
    >({
      query: (ingredientsAndPage) => ({
        url: '/recipe/search/',
        method: 'POST',
        body: ingredientsAndPage,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Request-Method': 'POST',
        },
      }),
    }),

    getRecipeListByNutrition: builder.mutation<
      RecipeListResponse,
      RecipeListNutritionRequest
    >({
      query: (nutritionAndPage) => ({
        url: '/recipe/search2/',
        method: 'POST',
        body: nutritionAndPage,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Request-Method': 'POST',
        },
      }),
    }),
  }),
})

export const {
  useGetRecipeListByIngredientsMutation,
  useGetRecipeListByNutritionMutation,
} = RecipeListSlice
