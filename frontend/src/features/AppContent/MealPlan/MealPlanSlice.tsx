import { Data } from 'ahooks/lib/usePagination/types'
import { apiSlice } from '../../api/apiSlice'
import { MealPlanDelete, MealPlanEntry, MealPlanUpdate } from '../../api/types'

const MealPlanSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getMealPlan: builder.query<MealPlanEntry[], number>({
      query: (userId) => `/meal-plan/${userId}`,
      providesTags: [{ type: 'MealPlan' }],
    }),
    updateMealPlan: builder.mutation<string, MealPlanUpdate>({
      query: (data) => {
        const { userId, ...body } = data

        return {
          url: `/meal-plan/${userId}`,
          method: 'PUT',
          body,
        }
      },
      invalidatesTags: [{ type: 'MealPlan' }],
    }),
    removeFromMealPlan: builder.mutation<string, MealPlanDelete>({
      query: (data) => ({
        url: `/meal-plan/delete/${data.userId}`,
        method: 'POST',
        body: data.day,
      }),
      invalidatesTags: [{ type: 'MealPlan' }],
    }),
  }),
})

export const {
  useGetMealPlanQuery,
  useUpdateMealPlanMutation,
  useRemoveFromMealPlanMutation,
} = MealPlanSlice
