import {
  Button,
  Divider,
  Grid2,
  IconButton,
  Paper,
  Typography,
} from '@mui/material'
import { Post } from './SocialMedia'
import { ThumbDownOutlined, ThumbUp } from '@mui/icons-material'

interface PostItemProp {
  post: Post
  index: number
}

const PostItem = (props: PostItemProp) => {
  const handleClickRecipe = (recipeId: number) => {
    console.log('Recipe Id: ', recipeId)
  }

  return (
    <Paper sx={{ mb: 2, height: '175px', borderRadius: 8 }} key={props.index}>
      <Grid2 container height="100%" columns={16}>
        <Grid2
          container
          size={4}
          direction={'column'}
          alignItems="center"
          justifyContent="center"
          height="100%"
        >
          <Button onClick={(e) => handleClickRecipe(props.post.recipeId)}>
            <Typography variant="h6">Recipe {props.post.recipeName}</Typography>
          </Button>
          {props.post.img ? (
            <img
              src={props.post.img}
              alt={`${props.post.recipeName} Image`}
              style={{
                maxWidth: '150px',
              }}
            />
          ) : (
            <></>
          )}
        </Grid2>
        <Grid2 container size={1}>
          <Divider orientation="vertical" />
        </Grid2>
        <Grid2 container alignItems="center" size={8} paddingY="30px">
          <Typography variant="body1" textAlign="left">
            {props.post.content}
          </Typography>
        </Grid2>
        <Grid2 size={1} container justifyContent="flex-end">
          <Divider orientation="vertical" />
        </Grid2>
        <Grid2
          container
          direction="column"
          size={2}
          alignItems="center"
          justifyContent="space-evenly"
        >
          <Grid2 size={6}>
            <IconButton>
              <ThumbUp />
            </IconButton>
          </Grid2>
          <Grid2 size={6}>
            <IconButton>
              <ThumbDownOutlined />
            </IconButton>
          </Grid2>
        </Grid2>
      </Grid2>
    </Paper>
  )
}

export default PostItem
