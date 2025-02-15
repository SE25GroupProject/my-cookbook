import { apiSlice } from '../../api/apiSlice'
import { Recipe } from '../../api/types'

export const RecipeInfoSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getRecipe: builder.query<Recipe, string>({
      query: (id) => `/recipe/${id}`,
    }),
  }),
})

export const { useGetRecipeQuery } = RecipeInfoSlice
