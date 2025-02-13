import { apiSlice } from '../../api/apiSlice'
import { User, UserCred, UserInfo } from '../../api/types'

export const userSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    login: builder.mutation<UserInfo, UserCred>({
      query: (user) => ({
        url: '/user/login',
        method: 'POST',
        body: user,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Request-Method': 'POST',
        },
      }),
    }),
    signup: builder.mutation<UserInfo, UserCred>({
      query: (user) => ({
        url: '/user/signup',
        method: 'POST',
        body: user,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Request-Method': 'POST',
        },
      }),
    }),
    getUser: builder.query<UserInfo, string>({
      query: (username) => ({
        url: `/user/getUser/${username}`,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Request-Method': 'GET',
        },
      }),
    }),
  }),
})

export const { useSignupMutation, useLoginMutation, useGetUserQuery } =
  userSlice
