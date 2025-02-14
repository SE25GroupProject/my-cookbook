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
  Container,
  Divider,
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
import { useEffect, useState } from 'react'
import InfiniteScroll from 'react-infinite-scroll-component'
import ImageInput from '../../../components/ImageInput'
import { FormProvider, useForm } from 'react-hook-form'
import { useAuth } from '../Authentication/AuthProvider'
import { useFixScroll } from './FixScroll'

interface Post {
  recipeId: number
  recipeName: string
  img: string
  content: string
}

interface PostRecipe {
  recipeId: number
  recipeName: string
}

const SocialMedia = () => {
  const auth = useAuth()
  const formMethods = useForm()

  const { handleSubmit, getValues } = formMethods

  const [posts, setPosts] = useState<Post[]>([
    {
      recipeId: 58,
      recipeName: 'Test 1',
      img: '',
      content: 'This is a test post',
    },
    {
      recipeId: 58,
      recipeName: 'Test 2',
      img: '',
      content: 'This is test post 2',
    },
    {
      recipeId: 58,
      recipeName: 'Test 3',
      img: '',
      content: 'This is test post 3',
    },
    {
      recipeId: 58,
      recipeName: 'Test 4',
      img: '',
      content: 'This is test post 4',
    },
    {
      recipeId: 58,
      recipeName: 'Test 5',
      img: '',
      content: 'This is test post 5',
    },
    {
      recipeId: 58,
      recipeName: 'Test 6',
      img: '',
      content: 'This is test post 6',
    },
    {
      recipeId: 58,
      recipeName: 'Test 7',
      img: '',
      content: 'This is test post 7',
    },
    {
      recipeId: 58,
      recipeName: 'Test 8',
      img: '',
      content: 'This is test post 9',
    },
    {
      recipeId: 58,
      recipeName: 'Test 10',
      img: '',
      content: 'This is test post 10',
    },
    {
      recipeId: 58,
      recipeName: 'Test 11',
      img: '',
      content: 'This is test post 11',
    },
    {
      recipeId: 58,
      recipeName: 'Test 12',
      img: '',
      content: 'This is test post 12',
    },
    {
      recipeId: 58,
      recipeName: 'Test 13',
      img: '',
      content: 'This is test post 13',
    },
    {
      recipeId: 58,
      recipeName: 'Test 14',
      img: '',
      content: 'This is test post 14',
    },
    {
      recipeId: 58,
      recipeName: 'Test 15',
      img: '',
      content: 'This is test post 15',
    },
    {
      recipeId: 58,
      recipeName: 'Test 16',
      img: '',
      content: 'This is test post 16',
    },
    {
      recipeId: 58,
      recipeName: 'Test 17',
      img: '',
      content: 'This is test post 17',
    },
    {
      recipeId: 58,
      recipeName: 'Test 18',
      img: '',
      content: 'This is test post 18',
    },
    {
      recipeId: 58,
      recipeName: 'Test 19',
      img: '',
      content: 'This is test post 19',
    },
    {
      recipeId: 58,
      recipeName: 'Test 20',
      img: '',
      content: 'This is test post 20',
    },
    {
      recipeId: 58,
      recipeName: 'Test 21',
      img: '',
      content: 'This is test post 21',
    },
    {
      recipeId: 58,
      recipeName: 'Test 22',
      img: '',
      content: 'This is test post 22',
    },
    {
      recipeId: 58,
      recipeName: 'Test 23',
      img: '',
      content: 'This is test post 23',
    },
  ])

  const userRecipes: PostRecipe[] = [
    {
      recipeId: 58,
      recipeName: 'test 1',
    },
    {
      recipeId: 58,
      recipeName: 'test 2',
    },
    {
      recipeId: 58,
      recipeName: 'test 3',
    },
    {
      recipeId: 58,
      recipeName: 'test 4',
    },
    {
      recipeId: 58,
      recipeName: 'test 5',
    },
  ]

  const [imgAnchorEl, setImgAnchorEl] = useState<HTMLButtonElement | null>(null)
  const [postImg, setPostImg] = useState('')

  const [chosenRecipe, setChosenRecipe] = useState<PostRecipe | null>(null)
  const [newPostText, setNewPostText] = useState('')

  const postsPerPage = 10

  const [currentPosts, setCurrentPosts] = useState<Post[]>(
    [...posts].splice(
      0,
      posts.length < postsPerPage ? posts.length : postsPerPage
    )
  )
  const [hasMore, setHasMore] = useState(true)

  const fetchData = () => {
    console.log('fetching!')

    if (posts.length == currentPosts.length) {
      setHasMore(false)
    }

    var postCopy = [...posts]
    var postsToDisplay = postCopy.splice(
      currentPosts.length,
      posts.length < postsPerPage ? posts.length : postsPerPage
    )

    console.log(posts.length)

    // a fake async api call like which sends
    // 20 more records in .5 secs
    setTimeout(() => {
      setCurrentPosts(currentPosts.concat(postsToDisplay))
    }, 1500)
  }

  useFixScroll(hasMore, fetchData)

  const handleClickRecipe = (recipeId: number) => {
    console.log('Recipe Id: ', recipeId)
  }

  const handleCreatePost = () => {
    if (chosenRecipe && newPostText) {
      let post: Post = {
        recipeId: chosenRecipe.recipeId,
        recipeName: chosenRecipe.recipeName,
        img: postImg,
        content: newPostText,
      }

      console.log(post)

      setPosts([...posts, post])
      setCurrentPosts([post, ...posts])

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
                getOptionLabel={(option) => option.recipeName}
                renderInput={(params) => (
                  <TextField {...params} label="Your Recipes" />
                )}
              />
            </Stack>

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
              placeholder="What's Cookin'?"
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
                <Paper
                  sx={{ mb: 2, height: '175px', borderRadius: 8 }}
                  key={index}
                >
                  <Grid2 container height="100%" columns={16}>
                    <Grid2
                      container
                      size={4}
                      direction={'column'}
                      alignItems="center"
                      justifyContent="center"
                      height="100%"
                    >
                      <Button onClick={(e) => handleClickRecipe(post.recipeId)}>
                        <Typography variant="h6">
                          Recipe {post.recipeName}
                        </Typography>
                      </Button>
                      {post.img ? (
                        <img
                          src={post.img}
                          alt={`${post.recipeName} Image`}
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
                    <Grid2
                      container
                      alignItems="center"
                      size={8}
                      paddingY="30px"
                    >
                      <Typography variant="body1" textAlign="left">
                        {post.content}
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
              ))}
            </InfiniteScroll>
          </Box>
        </Box>
      </Stack>
    </Container>
  )
}

export default SocialMedia
