import { apiSlice } from '../../api/apiSlice'
import { Post, PostRequest } from '../../api/types'

export const SocialSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getPosts: builder.query<Post[], void>({
      query: () => `/posts/`,
      providesTags: (result, error, arg) =>
        result
          ? // successful query
            [
              ...result.map(
                ({ postId }) => ({ type: 'Post', postId }) as const
              ),
              { type: 'Post', id: 'LIST' },
            ]
          : // an error occurred, but we still want to refetch this query when `{ type: 'Posts', id: 'LIST' }` is invalidated
            [{ type: 'Post', id: 'LIST' }],
    }),

    createPost: builder.mutation<string, PostRequest>({
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
      invalidatesTags: [{ type: 'Post', id: 'LIST' }],
    }),

    editPost: builder.mutation<Post, Partial<Post>>({
      query: (data) => {
        const { postId, ...body } = data
        return {
          url: `/posts/${postId}`,
          method: 'PUT',
          body,
        }
      },
      invalidatesTags: (result, error, { postId }) => [
        { type: 'Post', postId },
      ],
    }),

    deletePost: builder.mutation<string, Partial<Post>>({
      query: (data) => {
        const { postId, userId } = data
        return {
          url: `/posts/${postId}`,
          method: 'DELETE',
          body: userId,
        }
      },
      invalidatesTags: (result, error, postId) => [{ type: 'Post', postId }],
    }),
  }),
})

export const {
  useGetPostsQuery,
  useCreatePostMutation,
  useEditPostMutation,
  useDeletePostMutation,
} = SocialSlice
