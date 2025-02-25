import {
  Box,
  Card,
  Dialog,
  DialogContent,
  Grid2,
  IconButton,
  InputAdornment,
  OutlinedInput,
  Stack,
  Typography,
} from '@mui/material'
import { Post, PostComment } from '../../api/types'
import { Send } from '@mui/icons-material'
import CommentItem from './CommentItem'
import { useState } from 'react'

interface PostModalProps {
  post: Post
  isOpen: boolean
  handleClose: () => void
}

const PostModal = (props: PostModalProps) => {
  const [newCommentText, setNewCommentText] = useState('')

  const handleCreateComment = () => {
    if (newCommentText) {
      let comment: PostComment = {
        content: newCommentText,
        liked: false,
        disliked: false,
      }

      console.log(comment)

      setNewCommentText('')
    }
  }

  const handleModalClose = () => {
    setNewCommentText('')

    props.handleClose()
  }
  return (
    <Dialog
      open={props.isOpen}
      onClose={props.handleClose}
      fullWidth
      maxWidth="md"
    >
      <DialogContent>
        <Grid2 container spacing={2}>
          <Grid2 size={6}>
            <Stack spacing={2}>
              <Card sx={{ p: 1 }}>
                <Typography variant="h4" aria-label={'Modal Recipe Title'}>
                  Recipe {props.post.recipe.name}
                </Typography>
              </Card>

              {props.post.img ? (
                <img
                  src={props.post.img}
                  alt={`${props.post.recipe.name} Image`}
                  aria-label={'Modal Post Image'}
                  style={{
                    maxWidth: '150px',
                    maxHeight: '115px',
                  }}
                />
              ) : (
                <></>
              )}

              <Box>
                <Typography variant="body1">{props.post.content}</Typography>
              </Box>
            </Stack>
          </Grid2>
          <Grid2
            size={6}
            sx={{
              maxHeight: '80vh',
              overflow: 'hidden',
            }}
          >
            <Stack spacing={2}>
              <Box>
                <OutlinedInput
                  value={newCommentText}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                    setNewCommentText(e.target.value)
                  }}
                  size="small"
                  multiline
                  minRows={1}
                  maxRows={2}
                  fullWidth
                  id="whats-cookin"
                  label="Comment"
                  aria-label="Comment"
                  sx={{
                    '& fieldset': {
                      borderRadius: 8,
                    },
                  }}
                  endAdornment={
                    <InputAdornment position="end">
                      <IconButton
                        onClick={handleCreateComment}
                        disabled={!newCommentText}
                        aria-label="Submit Comment"
                      >
                        <Send />
                      </IconButton>
                    </InputAdornment>
                  }
                />
              </Box>
              <Stack
                spacing={2}
                sx={{
                  overflowY: 'auto',
                  pr: 3,
                  pl: 1,
                  width: '100%',
                }}
              >
                {props.post.comments.map((comment, index) => {
                  console.log(comment)
                  return <CommentItem comment={comment} index={index} />
                })}
              </Stack>
            </Stack>
          </Grid2>
        </Grid2>
      </DialogContent>
    </Dialog>
  )
}

export default PostModal
