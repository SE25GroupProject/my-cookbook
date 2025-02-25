import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  Grid2,
  IconButton,
  Paper,
  Stack,
  Typography,
} from '@mui/material'
import { Post, PostUpdate } from '../../api/types'
import {
  Comment,
  Delete,
  Edit,
  ThumbDown,
  ThumbDownOutlined,
  ThumbUp,
  ThumbUpOutlined,
} from '@mui/icons-material'
import { useAuth } from '../Authentication/AuthProvider'
import {
  useDeletePostMutation,
  useDislikePostMutation,
  useLikePostMutation,
} from './SocialSlice'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

interface PostItemProp {
  post: Post
  index: number
  openModalView: (post: Post) => void
  openModalEdit: (post: Post) => void
}

const PostItem = (props: PostItemProp) => {
  const auth = useAuth()
  const navigateTo = useNavigate()

  // Like and Dislike
  const userLiked = auth?.user
    ? props.post.likes.includes(auth?.user.id)
    : false
  const userDisliked = auth?.user
    ? props.post.dislikes.includes(auth?.user.id)
    : false

  const [likePost] = useLikePostMutation()
  const [dislikePost] = useDislikePostMutation()

  const handleLike = () => {
    if (auth) {
      let postUpdate: PostUpdate = {
        postId: props.post.postId,
        userId: auth?.user.id,
      }
      likePost(postUpdate)
    }
  }

  const handleDislike = () => {
    if (auth) {
      let postUpdate: PostUpdate = {
        postId: props.post.postId,
        userId: auth?.user.id,
      }
      dislikePost(postUpdate)
    }
  }

  // Recipe Click
  const handleClickRecipe = (recipeId: number) => {
    navigateTo('/recipe-details/' + recipeId)
  }

  // Delete and Delete Modal
  const [deleteModalOpen, setDeleteModalOpen] = useState(false)
  const [deletePost] = useDeletePostMutation()

  const handleCloseDeleteModal = () => {
    setDeleteModalOpen(false)
  }

  const handleDeletePost = () => {
    deletePost(props.post)
  }

  return (
    <Paper sx={{ mb: 2, height: '175px', borderRadius: 8 }} key={props.index}>
      <Grid2 container height="100%" columns={16}>
        <Grid2
          container
          size={4}
          direction={'column'}
          alignItems="flex-end"
          justifyContent="center"
          height="100%"
        >
          {props.post.image ? (
            <img
              src={props.post.image ?? null}
              alt={`${props.post.recipe.name} Image`}
              aria-label={'Post Image'}
              style={{
                maxWidth: '150px',
                maxHeight: '115px',
              }}
            />
          ) : (
            <></>
          )}
          <Divider orientation="vertical" />
        </Grid2>
        <Grid2 container alignItems="flex-start" size={10} padding="10px">
          <Stack spacing={2}>
            <Button
              onClick={(e) => handleClickRecipe(props.post.recipe.recipeId)}
              sx={{ p: 'unset' }}
            >
              <Typography
                variant="h6"
                aria-label={'Recipe Title'}
                textAlign={'left'}
              >
                {props.post.recipe.name ? props.post.recipe.name : 'Recipe'}
              </Typography>
            </Button>
            <Typography
              variant="body1"
              textAlign="left"
              aria-label={'Post Content'}
            >
              {props.post.message}
            </Typography>
          </Stack>
        </Grid2>
        <Grid2 size={1} container justifyContent="flex-end">
          <Divider orientation="vertical" />
        </Grid2>
        <Grid2
          container
          direction="column"
          size={1}
          alignItems="center"
          justifyContent="space-evenly"
        >
          {auth?.user.id == props.post.userId ? (
            <>
              <Grid2 container justifyContent={'center'} size={6}>
                <IconButton onClick={(e) => props.openModalEdit(props.post)}>
                  <Edit />
                </IconButton>
              </Grid2>
              <Grid2 container justifyContent={'center'} size={6}>
                <IconButton onClick={(e) => setDeleteModalOpen(true)}>
                  <Delete />
                </IconButton>
              </Grid2>
            </>
          ) : (
            <>
              <Grid2 size={4} container justifyContent={'center'}>
                <IconButton onClick={handleLike}>
                  {userLiked ? <ThumbUp /> : <ThumbUpOutlined />}
                </IconButton>
              </Grid2>
              <Grid2 size={4} container justifyContent={'center'}>
                <IconButton onClick={handleDislike}>
                  {userDisliked ? <ThumbDown /> : <ThumbDownOutlined />}
                </IconButton>
              </Grid2>
            </>
          )}
          <Grid2 size={4} container justifyContent={'center'}>
            <IconButton
              onClick={(e) => {
                props.openModalView(props.post)
              }}
            >
              <Comment />
            </IconButton>
          </Grid2>
        </Grid2>
      </Grid2>

      <Dialog open={deleteModalOpen} onClose={handleCloseDeleteModal}>
        <DialogTitle>
          <Typography>Are you sure?</Typography>
        </DialogTitle>
        <DialogContent>
          Are you sure you would like to delete this post: {props.post.message}
        </DialogContent>
        <DialogActions>
          <Button variant="outlined" onClick={handleCloseDeleteModal}>
            Cancel
          </Button>{' '}
          <Button variant="contained" onClick={handleDeletePost}>
            Confirm
          </Button>
        </DialogActions>
      </Dialog>
    </Paper>
  )
}

export default PostItem
