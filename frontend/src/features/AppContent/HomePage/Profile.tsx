import React, { useState } from 'react'
import './Profile.css' // Optional, for styling
import { useAuth } from '../../Authentication/AuthProvider'
import {
  Box,
  Button,
  Container,
  Dialog,
  Paper,
  Popover,
  Stack,
  Tooltip,
  Typography,
} from '@mui/material'
import ImageInput from '../../../components/ImageInput'
import { Form, FormProvider, useForm } from 'react-hook-form'
import avatar from './photos/default-avatar.png'

const Profile = () => {
  const auth = useAuth()
  const formMethods = useForm()
  const { handleSubmit, getValues } = formMethods
  const [imgAnchorEl, setImgAnchorEl] = useState<HTMLButtonElement | null>(null)

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
