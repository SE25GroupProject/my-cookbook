import {
  Autocomplete,
  Box,
  Button,
  Card,
  Dialog,
  DialogActions,
  DialogContent,
  Grid2,
  IconButton,
  InputAdornment,
  OutlinedInput,
  Paper,
  Popover,
  Stack,
  TextField,
  Tooltip,
  Typography,
} from '@mui/material'
import {
  Post,
  PostComment,
  PostCommentRequest,
  PostRecipe,
  PostRequest,
} from '../../api/types'
import { Send } from '@mui/icons-material'
import CommentItem from './CommentItem'
import { useEffect, useState } from 'react'
import { testRecipes } from '../testVariables'
import ImageInput from '../../../components/ImageInput'
import { FormProvider, useForm } from 'react-hook-form'
import { useAuth } from '../Authentication/AuthProvider'
import {
  useAddCommentMutation,
  useEditPostMutation,
  useGetPostByIdQuery,
} from './SocialSlice'
import { useNavigate } from 'react-router-dom'

interface PostModalProps {
  post: Post
  isOpen: boolean
  handleClose: () => void
  isEditMode: boolean
}

const PostModal = (props: PostModalProps) => {
  // Auth
  const auth = useAuth()
  const navigateTo = useNavigate()

  const { data: postRef } = useGetPostByIdQuery(props.post.postId)

  // Image Upload State
  const [imgAnchorEl, setImgAnchorEl] = useState<HTMLButtonElement | null>(null)
  const formMethods = useForm()
  const { handleSubmit, getValues } = formMethods

  // Available Recipes
  const userRecipes: PostRecipe[] = [...testRecipes]

  // Edit Post State
  const [editImg, setEditImg] = useState(props.post.image)
  const [chosenRecipe, setChosenRecipe] = useState<PostRecipe | null>(
    props.post.recipe
  )
  const [editMessage, setEditMessage] = useState(props.post.message)
  const [editPost, { isLoading: postEditLoading }] = useEditPostMutation()

  // Comments
  const [newCommentText, setNewCommentText] = useState('')
  const [addComment] = useAddCommentMutation()

  const handleCreateComment = () => {
    if (newCommentText && auth) {
      let comment: PostCommentRequest = {
        message: newCommentText,
        postId: props.post.postId,
        userId: auth?.user.id,
      }

      console.log(comment)

      addComment(comment)

      setNewCommentText('')
    }
  }

  // Recipe Click
  const handleClickRecipe = () => {
    navigateTo('/recipe-details/' + props.post.recipe.recipeId)
  }

  const handleModalClose = () => {
    setNewCommentText('')
    setChosenRecipe(null)
    setEditMessage('')
    setEditImg('')

    props.handleClose()
  }

  const handleEditPost = () => {
    if (editMessage && chosenRecipe && auth?.user?.id) {
      let post: PostRequest = {
        postId: props.post.postId,
        userId: auth?.user.id,
        recipe: chosenRecipe,
        image: editImg,
        message: editMessage,
      }

      editPost(post)
        .unwrap()
        .then((response) => {
          console.log(response)
        })
        .catch((err) => console.log(err))

      handleModalClose()
    }
  }

  const onImageChange = () => {
    const img = getValues('images')[0]
    setEditImg(img)
  }
  const handleClosePopup = () => {
    setImgAnchorEl(null)
  }

  return (
    <Dialog
      open={props.isOpen}
      onClose={props.handleClose}
      fullWidth
      maxWidth="md"
      slotProps={{ paper: { sx: { height: '100%' } } }}
    >
      {props.isEditMode ? (
        <>
          <DialogContent sx={{ height: 'inherit' }}>
            <Stack spacing={2}>
              <Card sx={{ p: 1 }}>
                <Autocomplete
                  fullWidth
                  value={chosenRecipe}
                  onChange={(event: any, newValue: PostRecipe | null) => {
                    setChosenRecipe(newValue)
                  }}
                  size="small"
                  options={userRecipes}
                  getOptionLabel={(option) => option.name}
                  renderInput={(params) => (
                    <TextField {...params} label="Your Recipes" />
                  )}
                />
              </Card>

              <Tooltip title="Click to Change Image" placement="top">
                <Button
                  onClick={(e) => {
                    setImgAnchorEl(e.currentTarget)
                  }}
                  sx={{ mr: 4 }}
                >
                  <img
                    src={editImg ?? null} // Fallback image if no profile photo
                    alt="edit Image"
                    className="edit-image"
                    style={{
                      width: '140px',
                    }}
                  />
                </Button>
              </Tooltip>

              <FormProvider {...formMethods}>
                <Popover
                  open={Boolean(imgAnchorEl)}
                  anchorEl={imgAnchorEl}
                  onClose={handleClosePopup}
                  anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'left',
                  }}
                  transformOrigin={{
                    vertical: 'top',
                    horizontal: 'left',
                  }}
                >
                  <Box
                    sx={{
                      ml: 4,
                      height: '150px',
                      display: 'flex',
                      justifyContent: 'center',
                      alignItems: 'center',
                      overflow: 'hidden',
                    }}
                  >
                    <ImageInput
                      images={[]}
                      multiple={false}
                      onChange={onImageChange}
                    />
                  </Box>
                </Popover>
              </FormProvider>

              <OutlinedInput
                value={editMessage}
                label={'Change Post Message'}
                aria-label="change post message"
                multiline
                minRows={4}
                maxRows={8}
                onChange={(e) => {
                  setEditMessage(e.target.value)
                }}
              />
            </Stack>
          </DialogContent>
          <DialogActions>
            <Button variant="outlined" onClick={handleModalClose}>
              Cancel
            </Button>
            <Button
              variant="contained"
              disabled={!editMessage}
              onClick={handleEditPost}
            >
              Edit Post
            </Button>
          </DialogActions>
        </>
      ) : (
        <DialogContent sx={{ height: 'inherit' }}>
          <Grid2 container spacing={2} sx={{ height: 'inherit' }}>
            <Grid2 size={6}>
              <Stack spacing={2}>
                <Card sx={{ p: 1 }}>
                  <Button variant="text" onClick={handleClickRecipe}>
                    <Typography variant="h4" aria-label={'Modal Recipe Title'}>
                      Recipe {props.post.recipe.name}
                    </Typography>
                  </Button>
                </Card>

                {props.post.image ? (
                  <img
                    src={props.post.image ?? null}
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
                  <Typography variant="body1">{props.post.message}</Typography>
                </Box>
              </Stack>
            </Grid2>
            <Grid2
              size={6}
              sx={{
                //   maxHeight: '80vh',
                overflow: 'hidden',
              }}
            >
              <Paper
                elevation={2}
                sx={{ height: 'calc(100% - 30px)', m: 1, p: 1 }}
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
                      maxHeight: '72vh',
                    }}
                  >
                    {postRef ? (
                      postRef.comments.map((comment, index) => {
                        return (
                          <CommentItem
                            comment={comment}
                            index={index}
                            postId={props.post.postId}
                            key={index}
                          />
                        )
                      })
                    ) : (
                      <></>
                    )}
                  </Stack>
                </Stack>
              </Paper>
            </Grid2>
          </Grid2>
        </DialogContent>
      )}
    </Dialog>
  )
}

export default PostModal
