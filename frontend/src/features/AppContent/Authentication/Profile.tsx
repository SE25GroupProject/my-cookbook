import React, { useEffect, useState } from 'react'
import './Profile.css' // Optional, for styling
import { useAuth } from './AuthProvider'
import {
  Box,
  Button,
  Container,
  Dialog,
  Paper,
  Popover,
  Stack,
  Tab,
  Tooltip,
  Typography,
} from '@mui/material'
import ImageInput from '../../../components/ImageInput'
import { Form, FormProvider, useForm } from 'react-hook-form'
import avatar from '../images/default-avatar.png'
import { TabContext, TabList, TabPanel } from '@mui/lab'
import { Post, PostRecipe, Recipe, RecipeListData } from '../../api/types'
import {
  mockRecipe,
  mockRecipeTwo,
  testPosts,
  testRecipes,
  testRecipesTwo,
} from '../testVariables'
import PostItem from '../SocialMedia/PostItem'
import InfiniteScroll from 'react-infinite-scroll-component'
import { useFixScroll } from '../SocialMedia/FixScroll'
import RecipeListItem from '../RecipeList/RecipeLIstItem'
import PostModal from '../SocialMedia/PostModal'
import { useGetPostsByUserQuery } from '../SocialMedia/SocialSlice'

const Profile = () => {
  const auth = useAuth()
  const formMethods = useForm()
  const { handleSubmit, getValues } = formMethods

  // Post View Modal
  const [postBeingViewed, setPostBeingViewed] = useState<Post | null>(null)
  const [postModalEditMode, setPostModalEditMode] = useState<boolean>(false)
  const postModalOpen = postBeingViewed ? true : false

  const handleOpenPostView = (post: Post) => {
    setPostBeingViewed(post)
    setPostModalEditMode(false)
  }

  const handleOpenPostEdit = (post: Post) => {
    setPostBeingViewed(post)
    setPostModalEditMode(true)
  }

  const handleClosePostView = () => {
    setPostBeingViewed(null)
  }

  // const myPosts: Post[] = [...testPosts]
  const userId = auth ? auth.user.id : -1
  const {
    data: myPosts,
    isLoading,
    isSuccess,
  } = useGetPostsByUserQuery(userId, { skip: userId == -1 })

  const userRecipes: Recipe[] = [mockRecipe, mockRecipeTwo]
  const favRecipes: Recipe[] = [mockRecipeTwo, mockRecipe]

  const postsPerPage = 10

  const [currentPosts, setCurrentPosts] = useState<Post[]>([])

  useEffect(() => {
    if (myPosts) {
      setCurrentPosts([...myPosts].splice(0, postsPerPage))
      console.log(myPosts)
    }
  }, [myPosts])

  const [hasMore, setHasMore] = useState(true)

  const fetchData = () => {
    if (myPosts) {
      if (myPosts.length == currentPosts.length) {
        setHasMore(false)
      }

      var postCopy = [...myPosts]
      var postsToDisplay = postCopy.splice(
        currentPosts.length,
        myPosts.length < postsPerPage ? myPosts.length : postsPerPage
      )

      // a fake async api call like which sends
      // 20 more records in .5 secs
      setTimeout(() => {
        setCurrentPosts(currentPosts.concat(postsToDisplay))
      }, 1500)
    }
  }

  useFixScroll(hasMore, fetchData)

  const [imgAnchorEl, setImgAnchorEl] = useState<HTMLButtonElement | null>(null)
  const [tabValue, setTabValue] = useState('1')

  // Sample user details
  const [profilePhoto, setProfilePhoto] = useState('')

  // State for file input (photo upload)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  // Handle file input changes (when user selects a photo)
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0])
    }
  }

  // Handle file upload (set the selected file as profile photo)
  const handleFileUpload = () => {
    if (selectedFile) {
      setProfilePhoto(
        URL.createObjectURL(selectedFile) // Generate a URL for the image
      )
    }
  }

  const onImageChange = () => {
    const img = getValues('images')[0]
    setProfilePhoto(img)
    console.log(img)
  }

  const handleClosePopup = () => {
    setImgAnchorEl(null)
  }

  const handleTabChange = (event: React.SyntheticEvent, newValue: string) => {
    setTabValue(newValue)
  }

  return (
    <Container fixed sx={{ height: 620 }}>
      <Paper elevation={3} sx={{ height: '100%' }}>
        <Stack>
          <Stack
            direction={'row'}
            alignItems={'center'}
            justifyContent={'left'}
          >
            <Tooltip title="Click to Change Image" placement="top">
              <Button
                onClick={(e) => {
                  setImgAnchorEl(e.currentTarget)
                }}
                sx={{ mr: 4 }}
              >
                <img
                  src={profilePhoto || avatar} // Fallback image if no profile photo
                  alt="Profile"
                  className="profile-photo"
                  style={{
                    width: '80px',
                    height: '80px',
                    borderRadius: '50%',
                    objectFit: 'cover',
                    marginBottom: '10px',
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
            <Typography
              variant="h3"
              textTransform={'capitalize'}
              aria-label="Users Name"
            >
              {auth?.user.username}'s Profile
            </Typography>
          </Stack>

          <TabContext value={tabValue}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <TabList
                onChange={handleTabChange}
                aria-label="lab API tabs example"
                variant="fullWidth"
              >
                <Tab label="My Posts" value="1" />
                <Tab label="My Favorites" value="2" />
                <Tab label="My Recipes" value="3" />
              </TabList>
            </Box>
            <TabPanel value="1" sx={{ p: 2 }}>
              <Box sx={{ overflow: 'hidden' }}>
                <Box
                  id="scrollable"
                  sx={{
                    height: 490,
                    width: '102%',
                    overflow: 'auto',
                    pr: '20px',
                  }}
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
                    scrollableTarget="scrollable"
                    height={440}
                  >
                    {currentPosts.map((post, index) => (
                      <PostItem
                        post={post}
                        index={index}
                        openModalView={handleOpenPostView}
                        openModalEdit={handleOpenPostEdit}
                      />
                    ))}
                  </InfiniteScroll>
                </Box>
              </Box>
            </TabPanel>
            <TabPanel value="2" sx={{ p: 2 }}>
              <Stack spacing={2} alignItems="center">
                {favRecipes.map((recipe, index) => (
                  <RecipeListItem recipe={recipe} index={index} />
                ))}
              </Stack>
            </TabPanel>
            <TabPanel value="3" sx={{ p: 2 }}>
              <Stack spacing={2} alignItems="center">
                {userRecipes.map((recipe, index) => (
                  <RecipeListItem recipe={recipe} index={index} />
                ))}
              </Stack>
            </TabPanel>
          </TabContext>
        </Stack>
      </Paper>

      {postBeingViewed ? (
        <PostModal
          post={postBeingViewed}
          isOpen={postModalOpen}
          handleClose={handleClosePostView}
          isEditMode={postModalEditMode}
        />
      ) : (
        <></>
      )}
    </Container>
  )
}

export default Profile
