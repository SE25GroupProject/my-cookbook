import {
  Button,
  Divider,
  Grid2,
  IconButton,
  Paper,
  Stack,
  Typography,
} from '@mui/material'
import { Post } from '../../api/types'
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
import { useDeletePostMutation } from './SocialSlice'

interface PostItemProp {
  post: Post
  index: number
  openModalView: (post: Post) => void
  openModalEdit: (post: Post) => void
}

const PostItem = (props: PostItemProp) => {
  const auth = useAuth()

  const userLiked = auth?.user
    ? props.post.likes.includes(auth?.user.id)
    : false
  const userDisliked = auth?.user
    ? props.post.dislikes.includes(auth?.user.id)
    : false

  const handleClickRecipe = (recipeId: number) => {
    console.log('Recipe Id: ', recipeId)
  }

  const [deletePost] = useDeletePostMutation()

  const handleDeletePost = () => {
    console.log('haha')
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
        <Grid2
          container
          alignItems="flex-start"
          size={auth?.user.id == props.post.userId ? 9 : 10}
          padding="10px"
        >
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
          <Grid2 size={4} container justifyContent={'center'}>
            <IconButton>
              {userLiked ? <ThumbUp /> : <ThumbUpOutlined />}
            </IconButton>
          </Grid2>
          <Grid2 size={4} container justifyContent={'center'}>
            <IconButton>
              {userDisliked ? <ThumbDown /> : <ThumbDownOutlined />}
            </IconButton>
          </Grid2>
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
        {auth?.user.id == props.post.userId ? (
          <Grid2 container direction="row" size={1} columns={12} spacing={0}>
            <Grid2 size={1}>
              <Divider orientation="vertical" />
            </Grid2>
            <Grid2
              container
              direction="column"
              alignItems="center"
              justifyContent="space-evenly"
              size={11}
            >
              <Grid2 container justifyContent={'center'} size={6}>
                <IconButton onClick={(e) => props.openModalEdit(props.post)}>
                  <Edit />
                </IconButton>
              </Grid2>
              <Grid2 container justifyContent={'center'} size={6}>
                <IconButton onClick={handleDeletePost}>
                  <Delete />
                </IconButton>
              </Grid2>
            </Grid2>
          </Grid2>
        ) : (
          <></>
        )}
      </Grid2>
    </Paper>
  )
}

export default PostItem
