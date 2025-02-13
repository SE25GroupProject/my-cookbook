import React, { useState } from 'react'
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

const Profile = () => {
  const auth = useAuth()
  const formMethods = useForm()
  const { handleSubmit, getValues } = formMethods
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
            <Typography variant="h3" textTransform={'capitalize'}>
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
              Post List
            </TabPanel>
            <TabPanel value="2" sx={{ p: 2 }}>
              My Favorites List
            </TabPanel>
            <TabPanel value="3" sx={{ p: 2 }}>
              My Recipes List
            </TabPanel>
          </TabContext>
        </Stack>
      </Paper>

      {/* <div
        className="profile-container"
        style={{ padding: '20px', textAlign: 'center' }}
      >
        <h2>Your Profile</h2>
      </div> */}
    </Container>
  )
}

export default Profile
