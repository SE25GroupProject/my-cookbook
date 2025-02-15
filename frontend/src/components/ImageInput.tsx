// Code Written by user Doannv97
// Code hosted on CodeSandbox: https://codesandbox.io/p/sandbox/material-ui-image-upload-component-9s8u0?file=%2Fsrc%2FImageUpload.js%3A1%2C1-133%2C1

// imports the React Javascript Library
import React, { useEffect, useState } from 'react'
//Card
import {
  Card,
  Button,
  Grid2,
  Avatar,
  withStyles,
  withTheme,
  Box,
  Typography,
  Pagination,
  IconButton,
  Tooltip,
} from '@mui/material'
// import Card from "@material-ui/core/Card";
// import Button from "@material-ui/core/Button";
// import Grid from "@material-ui/core/Grid";
// import Avatar from "@material-ui/core/Avatar";

//Tabs
// import { withStyles } from "@material-ui/core/styles";

const styles = (theme: any) => ({
  input: {
    display: 'none',
  },
  img: {
    width: 200,
    height: 256,
    margin: 'auto',
    display: 'block',
    maxWidth: '100%',
    maxHeight: '100%',
  },
})

import {
  Control,
  Controller,
  Field,
  FieldValues,
  useFormContext,
  UseFormRegister,
} from 'react-hook-form'
import { Recipe } from '../features/api/types'
import { ClearAll, DeleteOutline, Replay } from '@mui/icons-material'

interface ImageInputProps {
  images: Array<string> | undefined | null
  multiple: boolean
  onChange: (() => void) | null
}

const ImageInput = (props: ImageInputProps) => {
  const [files, setFiles] = useState<Array<string>>(props.images ?? [])
  const [page, setPage] = useState(props.images ? 1 : 0)
  const [selectedFile, setSelectedFile] = useState(props.images ? files[0] : '')

  const { register, control, setValue } = useFormContext()

  const triggerInputChange = (currentFiles: Array<string>) => {
    var input = document.querySelector('#contained-button-file')
    const inputValSetter = Object.getOwnPropertyDescriptor(
      window.HTMLInputElement.prototype,
      'value'
    )?.set
    inputValSetter?.call(input, currentFiles)
    const event = new Event('input', { bubbles: true })
    input?.dispatchEvent(event)
  }

  // const handleUploadClickDeprecated = (
  //   event: React.ChangeEvent<HTMLInputElement>,
  //   onChange: (...event: any[]) => void
  // ) => {
  //   if (Array.isArray(event.target.value)) {
  //     onChange([...event.target.value])
  //     return
  //   }

  //   var file = event.currentTarget.files?.item(0)

  //   if (!file) return

  //   const reader = new FileReader()

  //   reader.onloadend = () => {
  //     if (reader.result && typeof reader.result === 'string') {
  //       setFiles([...files, reader.result])
  //       onChange([...files, reader.result])

  //       if (!selectedFile) {
  //         setSelectedFile(reader.result)
  //         setPage(1)
  //       }
  //     }
  //   }
  //   reader.readAsDataURL(file)
  // }

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    var file = event.currentTarget.files?.item(0)
    if (!file) return

    const reader = new FileReader()

    reader.onloadend = () => {
      if (reader.result && typeof reader.result === 'string') {
        if (props.multiple) {
          setFiles([...files, reader.result])
          setValue('images', [...files, reader.result])
        } else {
          setFiles([reader.result])
          setSelectedFile(reader.result)
          setValue('images', [reader.result])
        }

        if (!selectedFile) {
          setSelectedFile(reader.result)
          setPage(1)
        }

        if (props.onChange) {
          props.onChange()
        }
      }
    }
    reader.readAsDataURL(file)
  }

  const removeCurrentImage = () => {
    if (page === 0) return

    var currentIdx = page - 1
    let currentFiles = files.filter((file, idx) => {
      return idx != currentIdx
    })

    setFiles(currentFiles)
    setValue('images', currentFiles)

    if (files.length != 0) {
      setPage(1)
      setSelectedFile(currentFiles[0])
    } else {
      setPage(0)
      setSelectedFile('')
    }
  }

  const removeAllImages = () => {
    setFiles([])
    setPage(0)
    setSelectedFile('')
    setValue('images', [])
  }

  const handlePageChange = (e: React.ChangeEvent<unknown>, newPage: number) => {
    setPage(newPage)
    setSelectedFile(files[newPage - 1])
  }

  return (
    <Box
      sx={{
        // width: '100%',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'flex-end',
      }}
    >
      {/* <Card className="img-card" sx={{ m: 2 }}> */}
      <Grid2 container direction="column" alignItems="center">
        <Tooltip title="Delete Current Image">
          <IconButton
            sx={{ position: 'absolute', top: 0, left: 0 }}
            onClick={removeCurrentImage}
          >
            <DeleteOutline />
          </IconButton>
        </Tooltip>
        <Tooltip title="Delete All Images">
          <IconButton
            sx={{ position: 'absolute', top: 40, left: 0 }}
            onClick={removeAllImages}
          >
            <ClearAll />
          </IconButton>
        </Tooltip>
        <label htmlFor="contained-button-file" style={{ margin: 10 }}>
          <Button component="span">
            <Grid2>
              {files.length > 0 ? (
                <img
                  width="100%"
                  style={{
                    width: 200,
                    height: 140,
                    margin: 'auto',
                    display: 'block',
                    maxWidth: '100%',
                    maxHeight: '100%',
                  }}
                  src={selectedFile}
                  alt={`Image ${page}`}
                />
              ) : (
                <Box
                // sx={{ mx: 2, my: 9 }}
                >
                  <Typography variant="subtitle1">
                    {' '}
                    Upload an image.{' '}
                  </Typography>
                </Box>
              )}
            </Grid2>
            <input
              accept="image/*"
              style={{ display: 'none' }}
              id="contained-button-file"
              type="file"
              onChange={handleImageUpload}
              aria-label="Upload Image Input"
            />

            {/* <Controller
              name={'images'}
              control={control}
              render={({ field }) => (
                <input
                  accept="image/*"
                  style={{ display: 'none' }}
                  id="contained-button-file"
                  type="file"
                  onChange={(event) => {
                    handleUploadClick(event, field.onChange)
                  }}
                  onBlur={field.onBlur}
                  ref={field.ref}
                  name={field.name}
                  multiple
                />
              )}
            /> */}
          </Button>

          {files.length > 0 && props.multiple ? (
            <Pagination
              page={page}
              count={files.length}
              color="secondary"
              sx={{ color: 'black' }}
              variant="outlined"
              onChange={handlePageChange}
              boundaryCount={1}
              siblingCount={0}
              // role="menu"
              // aria-label="image-pagination"
            />
          ) : (
            <></>
          )}
        </label>
      </Grid2>
      {/* </Card> */}
    </Box>
  )
}

export default ImageInput

// withStyles(styles, {withTheme:true})(ImageUploadCard)
