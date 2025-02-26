import { apiSlice } from '../../api/apiSlice'
import { FavoriteRequest, Recipe, UserRecipe } from '../../api/types'

export const UserRecipeSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getUserRecipes: builder.query<Recipe[], number>({
      query: (userId) => `/recipe/user/${userId}`,
    }),
    createUserRecipe: builder.mutation<Recipe, UserRecipe>({
      query: (data) => {
        const { userId, ...body } = data
        return {
          url: `/recipe/user/${userId}`,
          method: 'POST',
          body,
        }
      },
    }),
    editUserRecipe: builder.mutation<Recipe, UserRecipe>({
      query: (data) => {
        const { userId, ...body } = data
        return {
          url: `/recipe/user/${userId}`,
          method: 'PUT',
          body,
        }
      },
    }),
    getUserFavorites: builder.query<Recipe[], number>({
      query: (userId) => `/recipe/favorite/${userId}`,
      providesTags: [{ type: 'Favorite', id: 'LIST' }],
    }),
    checkUserFavorites: builder.query<boolean, FavoriteRequest>({
      query: (data) => `/recipe/favorite/${data.recipeId}/${data.userId}`,
      providesTags: (result, error, arg) =>
        !error
          ? // successful query
            [{ type: 'Favorite', id: arg.recipeId }]
          : [],
    }),
    favoriteRecipe: builder.mutation<boolean, FavoriteRequest>({
      query: (data) => ({
        url: `/recipe/favorite/${data.recipeId}/${data.userId}`,
        method: 'PUT',
      }),
      invalidatesTags: (result, error, args) =>
        !error
          ? [
              { type: 'Favorite', id: args.recipeId },
              { type: 'Favorite', id: 'LIST' },
            ]
          : [{ type: 'Favorite', id: 'LIST' }],
    }),
    unfavoriteRecipe: builder.mutation<boolean, FavoriteRequest>({
      query: (data) => ({
        url: `/recipe/unfavorite/${data.recipeId}/${data.userId}`,
        method: 'PUT',
      }),
      invalidatesTags: (result, error, args) =>
        !error
          ? [
              { type: 'Favorite', id: args.recipeId },
              { type: 'Favorite', id: 'LIST' },
            ]
          : [{ type: 'Favorite', id: 'LIST' }],
    }),
  }),
})

export const {
  useGetUserRecipesQuery,
  useCreateUserRecipeMutation,
  useEditUserRecipeMutation,
  useGetUserFavoritesQuery,
  useCheckUserFavoritesQuery,
  useFavoriteRecipeMutation,
  useUnfavoriteRecipeMutation,
} = UserRecipeSlice
