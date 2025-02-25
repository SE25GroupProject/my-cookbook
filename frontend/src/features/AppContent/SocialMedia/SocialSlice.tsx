import { apiSlice } from '../../api/apiSlice'
import {
  Post,
  PostComment,
  PostCommentRequest,
  PostRequest,
  PostUpdate,
} from '../../api/types'

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

    getPostsByUser: builder.query<Post[], number>({
      query: (userId) => `/posts/user/${userId}`,
      providesTags: (result, error, arg) =>
        result
          ? // successful query
            [...result.map(({ postId }) => ({ type: 'Post', postId }) as const)]
          : [],
    }),

    getPostById: builder.query<Post, number>({
      query: (postId) => `/posts/${postId}`,
      providesTags: (result, error, arg) =>
        result
          ? // successful query
            [{ type: 'Post', id: result.postId }]
          : [],
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

    deletePost: builder.mutation<string, PostUpdate>({
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

    likePost: builder.mutation<string, PostUpdate>({
      query: (data) => {
        const { postId, userId } = data
        return {
          url: `/posts/like/${postId}`,
          method: 'PUT',
          body: userId,
        }
      },
      invalidatesTags: (result, error, postId) => [{ type: 'Post', postId }],
    }),

    dislikePost: builder.mutation<string, PostUpdate>({
      query: (data) => {
        const { postId, userId } = data
        return {
          url: `/posts/dislike/${postId}`,
          method: 'PUT',
          body: userId,
        }
      },
      invalidatesTags: (result, error, postId) => [{ type: 'Post', postId }],
    }),

    addComment: builder.mutation<string, PostCommentRequest>({
      query: (data) => ({
        url: `/posts/comments/${data.postId}`,
        method: 'POST',
        body: data,
      }),
      invalidatesTags: (result, error, postId) => [{ type: 'Post', postId }],
    }),

    deleteComment: builder.mutation<string, PostComment>({
      query: (data) => ({
        url: `/posts/comments/${data.commentId}`,
        method: 'DELETE',
        body: data,
      }),
      invalidatesTags: (result, error, postId) => [{ type: 'Post', postId }],
    }),
  }),
})

export const {
  useGetPostsQuery,
  useCreatePostMutation,
  useEditPostMutation,
  useDeletePostMutation,
  useGetPostsByUserQuery,
  useGetPostByIdQuery,
  useLikePostMutation,
  useDislikePostMutation,
  useAddCommentMutation,
  useDeleteCommentMutation,
} = SocialSlice
