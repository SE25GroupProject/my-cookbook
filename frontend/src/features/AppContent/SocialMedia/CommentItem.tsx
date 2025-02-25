import {
  Button,
  Divider,
  Grid2,
  IconButton,
  Paper,
  Typography,
} from '@mui/material'
import { PostComment, Post } from '../../api/types'
import {
  Comment,
  ThumbDown,
  ThumbDownOutlined,
  ThumbUp,
  ThumbUpOutlined,
} from '@mui/icons-material'

interface CommentItemProp {
  comment: PostComment
  index: number
}

const CommentItem = (props: CommentItemProp) => {
  return (
    <Paper
      sx={{ mb: 2, pl: 1, height: '80px', borderRadius: 8 }}
      key={props.index}
    >
      <Grid2 container height="100%">
        <Grid2 container alignItems="center" size={8} paddingY="30px">
          <Typography
            variant="body1"
            textAlign="left"
            aria-label={'Comment Content'}
          >
            {props.comment.content}
          </Typography>
        </Grid2>
        <Grid2 size={1} container justifyContent="flex-end">
          <Divider orientation="vertical" />
        </Grid2>
        <Grid2
          container
          direction="row"
          size={3}
          alignItems="center"
          justifyContent="space-evenly"
        >
          <Grid2 size={6}>
            <IconButton>
              {props.comment.liked ? <ThumbUp /> : <ThumbUpOutlined />}
            </IconButton>
          </Grid2>
          <Grid2 size={6}>
            <IconButton>
              {props.comment.disliked ? <ThumbDown /> : <ThumbDownOutlined />}
            </IconButton>
          </Grid2>
        </Grid2>
      </Grid2>
    </Paper>
  )
}

export default CommentItem
