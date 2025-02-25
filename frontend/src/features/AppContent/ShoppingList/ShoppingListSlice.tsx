import { apiSlice } from '../../api/apiSlice'
import { ShoppingItem, ShoppingItemRequest } from '../../api/types'

export const ShoppingListSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getShoppingList: builder.query<ShoppingItem[], number>({
      query: (userId) => `/shopping-list/${userId}`,
      providesTags: [{ type: 'ShoppingList' }],
    }),

    updateShoppingList: builder.mutation<string, ShoppingItemRequest>({
      query: (data) => {
        const { userId, ...body } = data
        return {
          url: `/shopping-list/${userId}`,
          method: 'PUT',
          body,
        }
      },
      invalidatesTags: [{ type: 'ShoppingList' }],
    }),

    removeFromShoppingList: builder.mutation<string, ShoppingItemRequest>({
      query: (data) => {
        const { userId, name } = data

        return {
          url: `/shopping-list/delete/${userId}`,
          method: 'POST',
          body: name,
        }
      },
      invalidatesTags: [{ type: 'ShoppingList' }],
    }),
  }),
})

export const {
  useGetShoppingListQuery,
  useUpdateShoppingListMutation,
  useRemoveFromShoppingListMutation,
} = ShoppingListSlice
