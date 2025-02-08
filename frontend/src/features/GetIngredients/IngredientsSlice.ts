import { apiSlice } from '../api/apiSlice'

export const ingredientsSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getIngredientSuggestions: builder.query<string[], string>({
      query: (val) => ({
        url: `/recipe/ingredients/${val}`,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Request-Method': 'GET',
        },
      }),
    }),
  }),
})

export const { useGetIngredientSuggestionsQuery } = ingredientsSlice
