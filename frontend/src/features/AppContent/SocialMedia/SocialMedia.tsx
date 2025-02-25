import {
  Send,
  ThumbDown,
  ThumbDownAlt,
  ThumbDownOutlined,
  ThumbUp,
} from '@mui/icons-material'
import {
  Autocomplete,
  Box,
  Button,
  Card,
  Container,
  Dialog,
  DialogContent,
  DialogContentText,
  Divider,
  Grid2,
  IconButton,
  InputAdornment,
  InputLabel,
  OutlinedInput,
  Paper,
  Popover,
  Stack,
  TextField,
  Tooltip,
  Typography,
} from '@mui/material'
import { useEffect, useState } from 'react'
import InfiniteScroll from 'react-infinite-scroll-component'
import ImageInput from '../../../components/ImageInput'
import { FormProvider, useForm } from 'react-hook-form'
import { useAuth } from '../Authentication/AuthProvider'
import { useFixScroll } from './FixScroll'
import PostItem from './PostItem'
import { testPosts, testRecipes } from '../testVariables'
import { Post, PostComment, PostRecipe } from '../../api/types'
import CommentItem from './CommentItem'
import PostModal from './PostModal'
import { useCreatePostMutation, useGetPostsQuery } from './SocialSlice'

const SocialMedia = () => {
  const auth = useAuth()
  const formMethods = useForm()

  const { handleSubmit, getValues } = formMethods

  // const [posts, setPosts] = useState<Post[]>([...testPosts])
  const { data: posts, isLoading, isSuccess } = useGetPostsQuery()
  const userRecipes: PostRecipe[] = [...testRecipes]

  // Post creation
  const [imgAnchorEl, setImgAnchorEl] = useState<HTMLButtonElement | null>(null)
  const [postImg, setPostImg] = useState('')
  const [chosenRecipe, setChosenRecipe] = useState<PostRecipe | null>(null)
  const [newPostText, setNewPostText] = useState('')
  const [createPost, { isLoading: postCreationLoading }] =
    useCreatePostMutation()

  // Post View Modal
  const [postBeingViewed, setPostBeingViewed] = useState<Post | null>(null)
  const postModalOpen = postBeingViewed ? true : false

  const handleOpenPostView = (post: Post) => {
    setPostBeingViewed(post)
  }

  const handleClosePostView = () => {
    setPostBeingViewed(null)
  }

  // Post endless scroll
  const postsPerPage = 10

  const [currentPosts, setCurrentPosts] = useState<Post[]>(
    posts
      ? [...posts].splice(
          0,
          posts.length < postsPerPage ? posts.length : postsPerPage
        )
      : []
  )
  const [hasMore, setHasMore] = useState(true)

  const fetchData = () => {
    if (posts) {
      if (posts.length == currentPosts.length) {
        setHasMore(false)
      }

      var postCopy = [...posts]
      var postsToDisplay = postCopy.splice(
        currentPosts.length,
        posts.length < postsPerPage ? posts.length : postsPerPage
      )

      // a fake async api call like which sends
      // 20 more records in .5 secs
      setTimeout(() => {
        setCurrentPosts(currentPosts.concat(postsToDisplay))
      }, 1500)
    }
  }

  useFixScroll(hasMore, fetchData)

  const handleCreatePost = () => {
    if (chosenRecipe && newPostText) {
      let post: Post = {
        postId: -1,
        recipe: chosenRecipe,
        img: postImg,
        content: newPostText,
        liked: false,
        disliked: false,
        comments: [],
      }

      console.log(post)

      // setPosts([...posts, post])
      // setCurrentPosts([post, ...posts])

      createPost(post)
        .unwrap()
        .then((response: string) => {
          console.log(response)
        })
        .catch((err) => console.log(err))

      setChosenRecipe(null)
      setNewPostText('')
      setPostImg('')
    }
  }

  const onImageChange = () => {
    const img = getValues('images')[0]
    setPostImg(img)
  }

  const handleClosePopup = () => {
    setImgAnchorEl(null)
  }

  return (
    <Container maxWidth="md" sx={{ pt: 2 }}>
      <Stack spacing={2}>
        <Paper sx={{ p: 2, borderRadius: 8 }}>
          <Stack spacing={1}>
            <Stack direction="row" spacing={2} alignItems="flex-end">
              <Tooltip title="Click to Change Image" placement="top">
                <Button
                  onClick={(e) => {
                    setImgAnchorEl(e.currentTarget)
                  }}
                  sx={{ mr: 4 }}
                >
                  <img
                    src={postImg} // Fallback image if no profile photo
                    alt="Recipe Image"
                    className="recipe-image"
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
            </Stack>

            <InputLabel htmlFor="whats-cookin" sx={{ visibility: 'hidden' }}>
              What's Cookin'?
            </InputLabel>
            <OutlinedInput
              value={newPostText}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                setNewPostText(e.target.value)
              }}
              size="small"
              multiline
              minRows={1}
              maxRows={4}
              fullWidth
              id="whats-cookin"
              placeholder="What's Cookin'?"
              label="What's Cookin'?"
              aria-label="What's Cookin'?"
              sx={{
                '& fieldset': {
                  borderRadius: 8,
                },
              }}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    onClick={handleCreatePost}
                    disabled={!(chosenRecipe && newPostText)}
                    aria-label="Submit Recipe"
                  >
                    <Send />
                  </IconButton>
                </InputAdornment>
              }
            />
          </Stack>
        </Paper>
        <Box sx={{ overflow: 'hidden' }}>
          <Box
            id="scrollableDiv"
            sx={{ height: 490, width: '102%', overflow: 'auto', pr: '20px' }}
          >
            <InfiniteScroll
              dataLength={currentPosts.length}
              next={fetchData}
              hasMore={hasMore}
              loader={<h4>Loading...</h4>}
              endMessage={
                <p style={{ textAlign: 'center' }}>
                  <b>Yay! You have seen it all</b>
                </p>
              }
              scrollableTarget="scrollableDiv"
            >
              {currentPosts.map((post, index) => (
                <PostItem
                  post={post}
                  index={index}
                  openModal={handleOpenPostView}
                />
              ))}
            </InfiniteScroll>
          </Box>
          {postBeingViewed ? (
            <PostModal
              post={postBeingViewed}
              isOpen={postModalOpen}
              handleClose={handleClosePostView}
            />
          ) : (
            <></>
          )}
        </Box>
      </Stack>
    </Container>
  )
}

export default SocialMedia
