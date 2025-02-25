import { apiSlice } from '../../api/apiSlice'
import { Post } from '../../api/types'

export const SocialSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getPosts: builder.query<Post[], void>({
      query: () => `/posts/`,
      providesTags: (result, error, arg) =>
        result
          ? [
              ...result.map(({ postId }) => ({
                type: 'Post' as const,
                id: postId,
              })),
              'Post',
            ]
          : ['Post'],
    }),

    createPost: builder.mutation<string, Post>({
      query: (post) => ({
        url: '/posts/',
        method: 'POST',
        body: post,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Request-Method': 'POST',
        },
      }),
      invalidatesTags: ['Post'],
    }),
  }),
})

export const { useGetPostsQuery, useCreatePostMutation } = SocialSlice
