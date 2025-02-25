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
  Delete,
  ThumbDown,
  ThumbDownOutlined,
  ThumbUp,
  ThumbUpOutlined,
} from '@mui/icons-material'
import { useAuth } from '../Authentication/AuthProvider'
import { useDeleteCommentMutation } from './SocialSlice'

interface CommentItemProp {
  comment: PostComment
  postId: number
  index: number
}

const CommentItem = (props: CommentItemProp) => {
  const auth = useAuth()

  const [deleteComment] = useDeleteCommentMutation()
  const handleDelete = () => {
    deleteComment(props.comment)
  }

  return (
    <Paper
      sx={{ mb: 2, pl: 1, padding: '25px 20px', borderRadius: 8 }}
      key={props.index}
    >
      <Grid2 container height="100%">
        <Grid2
          container
          alignItems="center"
          size={auth?.user.id == props.comment.userId ? 8 : 12}
          paddingY="30px"
        >
          <Typography
            variant="body1"
            textAlign="left"
            aria-label={'Comment Content'}
            overflow={'hidden'}
            textOverflow={'ellipsis'}
            maxHeight={'100px'}
          >
            {props.comment.message}
          </Typography>
        </Grid2>
        {auth?.user.id == props.comment.userId ? (
          <>
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
              <IconButton onClick={handleDelete}>
                <Delete />
              </IconButton>
            </Grid2>
          </>
        ) : (
          <></>
        )}
      </Grid2>
    </Paper>
  )
}

export default CommentItem
