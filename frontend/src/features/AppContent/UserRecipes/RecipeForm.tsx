/*

Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com

*/

import { useParams } from 'react-router-dom'
import { useGetRecipeQuery } from '../../api/apiSlice'
import React, { useEffect, useState } from 'react'
import { Recipe, RecipeObject, UserRecipe } from '../../api/types'
import { Controller, Form, FormProvider, useForm } from 'react-hook-form'
import {
  Box,
  Button,
  Container,
  Grid2,
  IconButton,
  InputAdornment,
  OutlinedInput,
  Paper,
  Stack,
  styled,
  Tab,
  TextField,
  Tooltip,
  Typography,
  TablePagination,
  Autocomplete,
  Popover,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material'
import ImageInput from '../../../components/ImageInput'
import { useTheme } from '../../Themes/themeContext'
import { TabContext, TabList, TabPanel } from '@mui/lab'
import {
  AddCircleOutline,
  Close,
  DeleteOutline,
  Description,
  Edit,
  HelpOutline,
  QuestionMark,
  Replay,
} from '@mui/icons-material'
import { RECIPE_CATEGORIES } from '../RecipeList/recipeCategories'
import {
  useCreateUserRecipeMutation,
  useEditUserRecipeMutation,
} from './UserRecipeSlice'
import { useAuth } from '../Authentication/AuthProvider'

/**
 * File name: RecipeForm.tsx
 * Task - This component allows users to generate or update user submitted recipes via a form.
 * @author Camille Jones - crjone24@gmail.com
 */

interface RecipeFormProps {
  recipe: Recipe | null
}

interface Time {
  hour: number
  min: number
}

const transformStringToTime = (timeString: string): Time => {
  const timeRegex = /^(?!\s*$)+(([\d]*)[H]{1})?(([\d]*)[M]{1})?/gm

  const timeParsed = timeRegex.exec(timeString)
  return {
    hour: parseInt(timeParsed?.[2] ?? '0'),
    min: parseInt(timeParsed?.[4] ?? '0'),
  }
}

const transformTimeToString = (time: Time): string => {
  const hours = time.hour > 0 ? `${time.hour}H` : ''
  const mins = time.min > 0 ? `${time.min}M` : ''
  return hours || mins ? hours + mins : '~'
}

const RecipeForm = () => {
  const { id } = useParams()
  const { theme } = useTheme()
  const auth = useAuth()
  const [tabValue, setTabValue] = useState('1')
  const [forceShrink, setForceShrink] = useState(true)

  const [prepTime, setPrepTime] = useState<Time>({ min: 0, hour: 0 })
  const [cookTime, setCookTime] = useState<Time>({ min: 0, hour: 0 })
  const [totalTime, setTotalTime] = useState<Time>({ min: 0, hour: 0 })

  const [ingredients, setIngredients] = useState<Array<string>>([])
  const [ingPage, setIngPage] = useState(0)
  const [ingToAdd, setIngToAdd] = useState('')
  const ingPerPage = 3
  const currIngs = ingredients.slice(
    ingPage * ingPerPage,
    ingPage * ingPerPage + ingPerPage
  )

  const [steps, setSteps] = useState<Array<string>>([])
  const [stepPage, setStepPage] = useState(0)
  const [stepToAdd, setStepToAdd] = useState('')
  const stepsPerPage = 5
  const currSteps = steps.slice(
    stepPage * stepsPerPage,
    stepPage * stepsPerPage + stepsPerPage
  )

  const [stepToEdit, setStepToEdit] = useState('')
  const [stepToEditIdx, setStepToEditIdx] = useState(-1)
  const [anchorEl, setAnchorEl] = React.useState<HTMLButtonElement | null>(null)
  const openStepAdd = Boolean(anchorEl)
  const [createRecipe] = useCreateUserRecipeMutation()
  const [editRecipe] = useEditUserRecipeMutation()

  const handleOpenAddStepPopup = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    setAnchorEl(event.currentTarget)
  }

  const handleCloseAddStepPopup = () => {
    setAnchorEl(null)
  }

  const [openStepEdit, setOpenStepEdit] = useState(false)
  const handleOpenEditStepPopup = (
    event: React.MouseEvent<HTMLButtonElement> | null,
    index: number
  ) => {
    console.log('index', index)
    const fullIndex = stepPage * stepsPerPage + index
    setStepToEdit(steps[fullIndex])
    setStepToEditIdx(fullIndex)
    setOpenStepEdit(true)
  }

  const handleCloseEditStepPopup = () => {
    setStepToEdit('')
    setOpenStepEdit(false)
  }

  let defaultUserRecipe: Recipe | undefined = new RecipeObject()

  const formMethods = useForm<Recipe>({ defaultValues: defaultUserRecipe })
  const { handleSubmit, control, reset, register } = formMethods

  const {
    data: recipe,
    isLoading,
    isSuccess,
  } = useGetRecipeQuery(id as string, { skip: typeof id === 'undefined' })

  useEffect(() => {
    if (recipe) {
      reset(recipe)
      setForceShrink(true)

      setPrepTime(transformStringToTime(recipe.prepTime))
      setCookTime(transformStringToTime(recipe.cookTime))
      setIngredients(recipe.ingredients)
      setSteps(recipe.instructions.map((inst) => inst.instruction))
    }
  }, [reset, recipe])

  useEffect(() => {
    var hours = prepTime.hour + cookTime.hour
    var mins = prepTime.min + cookTime.min

    if (mins > 59) {
      hours = hours + 1
      mins = mins - 60
    }

    setTotalTime({
      hour: hours,
      min: mins,
    })
  }, [prepTime, cookTime])

  const handleTabChange = (event: React.SyntheticEvent, newValue: string) => {
    setTabValue(newValue)
  }

  const onSubmit = handleSubmit((data) => {
    if (!auth) return

    data.prepTime = transformTimeToString(prepTime)
    data.cookTime = transformTimeToString(cookTime)
    data.totalTime = transformTimeToString(totalTime)

    data.ingredients = ingredients
    data.instructions = steps.map((inst, index) => ({
      step: index,
      instruction: inst,
    }))

    let userRecipe: UserRecipe = {
      userId: auth.user.id,
      name: data.name ?? '',
      cookTime: data.cookTime ?? '',
      prepTime: data.prepTime ?? '',
      totalTime: data.totalTime ?? '',
      description: data.description ?? '',
      category: data.category ?? '',
      rating: data.rating ?? 5,
      calories: data.calories ?? 0,
      fat: data.fat ?? 0,
      saturatedFat: data.saturatedFat ?? 0,
      cholesterol: data.cholesterol ?? 0,
      sodium: data.sodium ?? 0,
      carbs: data.carbs ?? 0,
      fiber: data.fiber ?? 0,
      sugar: data.sugar ?? 0,
      protein: data.protein ?? 0,
      servings: data.servings ?? 0,
      images: data.images ?? [],
      tags: data.tags ?? [],
      ingredientQuantities: [],
      ingredients: data.ingredients ?? [],
      instructions: data.instructions ?? [],
    }

    console.log(userRecipe)

    // Edit
    if (id) {
      editRecipe(userRecipe)
        .unwrap()
        .then((response) => {
          alert(`Succesfully Edited ${userRecipe.name}`)
        })
        .catch((err) => {
          console.log(err)
          alert(`Error! Unable to edit recipe.`)
        })

      // Create
    } else {
      createRecipe(userRecipe)
        .unwrap()
        .then((response) => {
          alert(`Succesfully Created ${userRecipe.name}`)
        })
        .catch((err) => {
          console.log(err)
          alert(`Error! Unable to create recipe.`)
        })
    }
  })

  const onTimeChanged = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
    type: 'prep' | 'cook',
    isHours: boolean
  ) => {
    const value = parseInt(e.target.value)
    const boundedValue = value > 60 ? 60 : value < 0 ? 0 : value

    if (type === 'prep') {
      setPrepTime({
        min: isHours ? prepTime.min : boundedValue,
        hour: isHours ? boundedValue : prepTime.hour,
      })
    } else {
      setCookTime({
        min: isHours ? cookTime.min : boundedValue,
        hour: isHours ? boundedValue : cookTime.hour,
      })
    }
  }

  const handleIngChangeAddInput = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setIngToAdd(event.target.value)
  }

  const handleIngredientAdd = () => {
    setIngredients([...ingredients, ingToAdd])
    setIngToAdd('')
  }

  const handleIngredientRemove = (index: number) => {
    const fullIndex = ingPage * ingPerPage + index
    const newIngList = ingredients.filter((ing, idx) => {
      return idx != fullIndex
    })
    setIngredients(newIngList)

    if (ingPage != 0 && ingPage * ingPerPage + 1 > newIngList.length)
      setIngPage(ingPage - 1)
  }

  const handleIngChangePage = (
    event: React.MouseEvent<HTMLButtonElement> | null,
    page: number
  ) => {
    setIngPage(page)
  }

  const handleStepChangeAddInput = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setStepToAdd(event.target.value)
  }

  const handleStepChangeEditInput = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setStepToEdit(event.target.value)
  }

  const handleStepAdd = () => {
    setSteps([...steps, stepToAdd])
    setStepToAdd('')
    handleCloseAddStepPopup()
  }

  const handleStepEdit = (index: number) => {
    // console.log('index', index)
    // const fullIndex = stepPage * stepsPerPage + index
    // console.log('full index', fullIndex)
    setSteps(
      steps.map((step, idx) => {
        return idx === stepToEditIdx ? stepToEdit : step
      })
    )
    setStepToEdit('')
    handleCloseEditStepPopup()
  }

  const handleStepRemove = (index: number) => {
    const fullIndex = stepPage * stepsPerPage + index
    const newStepsList = steps.filter((step, idx) => {
      return idx != fullIndex
    })
    setSteps(newStepsList)

    if (stepPage != 0 && stepPage * stepsPerPage + 1 > newStepsList.length)
      setIngPage(ingPage - 1)
  }

  const handleStepChangePage = (
    event: React.MouseEvent<HTMLButtonElement> | null,
    page: number
  ) => {
    setStepPage(page)
  }

  return (
    <Container maxWidth="lg">
      {isLoading ? (
        <Typography variant="body1">Loading...</Typography>
      ) : (
        <>
          <Typography
            variant="h4"
            align="left"
            gutterBottom
            color={theme.color}
          >
            {id ? 'Edit' : 'Create'} Recipe
          </Typography>
          <Paper
            elevation={6}
            sx={{ height: { xs: 300, sm: 340, md: 575, xl: 680 } }}
          >
            <FormProvider {...formMethods}>
              <Box
                className="recipe-form"
                style={{ padding: '20px' }}
                onSubmit={onSubmit}
                component={'form'}
              >
                <Grid2 container spacing={2}>
                  <Grid2 size={5}>
                    <Stack
                      spacing={2}
                      sx={{
                        alignItems: 'stretch',
                      }}
                    >
                      <Paper
                        elevation={3}
                        sx={{
                          textAlign: 'center',
                          height: '200px',
                          position: 'relative',
                          display: 'flex',
                          justifyContent: 'center',
                          alignItems: 'center',
                        }}
                      >
                        <Tooltip
                          title="Click Image to Choose New Image"
                          sx={{ position: 'absolute', top: 0, right: 0 }}
                        >
                          <IconButton>
                            <HelpOutline></HelpOutline>
                          </IconButton>
                        </Tooltip>
                        <ImageInput
                          images={recipe ? recipe.images : null}
                          multiple={true}
                          onChange={null}
                        />
                      </Paper>
                      <Paper
                        elevation={3}
                        sx={{
                          textAlign: 'center',
                          height: { lg: 315, xl: 425 },
                        }}
                      >
                        <TabContext value={tabValue}>
                          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                            <TabList
                              onChange={handleTabChange}
                              aria-label="lab API tabs example"
                              variant="fullWidth"
                            >
                              <Tab label="Desc." value="1" />
                              <Tab label="Info" value="2" />
                              <Tab label="Ing." value="3" />
                              <Tab label="Nutr." value="4" />
                            </TabList>
                          </Box>
                          <TabPanel value="1" sx={{ p: 2 }}>
                            <Grid2 container spacing={2}>
                              <Controller
                                name="category"
                                control={control}
                                render={({ field: { onChange, value } }) => (
                                  <Autocomplete
                                    onChange={(event, item) => {
                                      onChange(item)
                                    }}
                                    value={value}
                                    options={RECIPE_CATEGORIES}
                                    getOptionLabel={(option) => option || ''}
                                    // onInputChange={(e, v) => field.onChange(v)}
                                    renderInput={(params) => (
                                      <TextField
                                        {...params}
                                        // inputRef={field.ref}
                                        // error={fieldState.invalid}
                                        label="Category"
                                      />
                                    )}
                                    clearOnEscape
                                    autoHighlight
                                    // value={field.value || ''}
                                    // onBlur={field.onBlur}
                                    // onChange={(e, data) => onChange}
                                    // ref={field.ref}
                                    fullWidth
                                  ></Autocomplete>
                                )}
                              />
                              <Controller
                                name="description"
                                rules={{ required: true }}
                                render={({ field }) => (
                                  <TextField
                                    id="standard-multiline-static"
                                    label="Description"
                                    multiline
                                    maxRows={8}
                                    {...field}
                                    fullWidth
                                    slotProps={{
                                      inputLabel: { shrink: forceShrink },
                                    }}
                                  />
                                )}
                              />
                            </Grid2>
                          </TabPanel>
                          <TabPanel value="2">
                            <Grid2 container spacing={2}>
                              <Grid2 size={12}>
                                <Controller
                                  name="servings"
                                  rules={{ required: true }}
                                  render={({ field }) => (
                                    <TextField
                                      label="Servings"
                                      type="number"
                                      {...field}
                                      fullWidth
                                      slotProps={{
                                        inputLabel: { shrink: forceShrink },
                                      }}
                                      size="small"
                                    />
                                  )}
                                />
                              </Grid2>
                              <Grid2 size={6}>
                                <TextField
                                  label="Prep Hours"
                                  type="number"
                                  slotProps={{
                                    inputLabel: { shrink: forceShrink },
                                  }}
                                  size="small"
                                  value={prepTime?.hour}
                                  onChange={(e) =>
                                    onTimeChanged(e, 'prep', true)
                                  }
                                />
                              </Grid2>
                              <Grid2 size={6}>
                                <TextField
                                  label="Prep Mins"
                                  type="number"
                                  slotProps={{
                                    inputLabel: { shrink: forceShrink },
                                  }}
                                  size="small"
                                  value={prepTime?.min}
                                  onChange={(e) =>
                                    onTimeChanged(e, 'prep', false)
                                  }
                                />
                              </Grid2>
                              <Grid2 size={6}>
                                <TextField
                                  label="Cook Hours"
                                  type="number"
                                  slotProps={{
                                    inputLabel: { shrink: forceShrink },
                                  }}
                                  size="small"
                                  value={cookTime?.hour}
                                  onChange={(e) =>
                                    onTimeChanged(e, 'cook', true)
                                  }
                                />
                              </Grid2>
                              <Grid2 size={6}>
                                <TextField
                                  label="Cook Mins"
                                  type="number"
                                  slotProps={{
                                    inputLabel: { shrink: forceShrink },
                                  }}
                                  size="small"
                                  value={cookTime?.min}
                                  onChange={(e) =>
                                    onTimeChanged(e, 'cook', false)
                                  }
                                />
                              </Grid2>
                              <Grid2 size={6}>
                                <Typography variant="h6" textAlign={'left'}>
                                  Total:
                                </Typography>
                              </Grid2>
                              <Grid2 size={6}>
                                <Typography variant="h6" textAlign={'right'}>
                                  {totalTime.hour ?? 0} H {totalTime.min ?? 0} M
                                </Typography>
                              </Grid2>
                            </Grid2>
                          </TabPanel>
                          <TabPanel value="3" sx={{ px: 2, py: 1 }}>
                            <OutlinedInput
                              id="outlined-adornment-password"
                              endAdornment={
                                <InputAdornment position="end">
                                  <IconButton
                                    onClick={handleIngredientAdd}
                                    edge="end"
                                    aria-label="Add New Ingredient"
                                    disabled={
                                      ingToAdd.length === 0 ||
                                      ingredients.includes(ingToAdd)
                                    }
                                  >
                                    <AddCircleOutline />
                                  </IconButton>
                                </InputAdornment>
                              }
                              size="small"
                              fullWidth
                              sx={{ mb: 2 }}
                              value={ingToAdd}
                              onChange={handleIngChangeAddInput}
                              aria-label="Add Ingredient Input"
                            />
                            <Stack spacing={1} sx={{ minHeight: 142 }}>
                              {currIngs.map((currIng, index) => (
                                <Container
                                  aria-label={`Ingredient ${ingPage * ingPerPage + index}`}
                                  key={index}
                                  sx={{
                                    px: 2,
                                    py: 1,
                                    border: '1px solid',
                                    borderColor: 'divider',
                                    borderRadius: 2,
                                    position: 'relative',
                                  }}
                                >
                                  <Typography variant="body1">
                                    {currIng}
                                  </Typography>
                                  <IconButton
                                    onClick={() => {
                                      handleIngredientRemove(index)
                                    }}
                                    sx={{
                                      position: 'absolute',
                                      right: 0,
                                      top: 0,
                                      bottom: 0,
                                    }}
                                  >
                                    <DeleteOutline />
                                  </IconButton>
                                </Container>
                              ))}
                            </Stack>

                            <TablePagination
                              component="div"
                              count={ingredients.length}
                              page={ingPage}
                              onPageChange={handleIngChangePage}
                              rowsPerPage={3}
                              rowsPerPageOptions={[]}
                            />
                          </TabPanel>
                          <TabPanel value="4">
                            <Grid2 container spacing={1}>
                              <Grid2 size={12}>
                                <Controller
                                  name="calories"
                                  rules={{ required: true }}
                                  render={({ field }) => (
                                    <TextField
                                      label="Calories"
                                      {...field}
                                      fullWidth
                                      slotProps={{
                                        inputLabel: { shrink: forceShrink },
                                        htmlInput: {
                                          step: '.1',
                                        },
                                      }}
                                      type="number"
                                      size="small"
                                    />
                                  )}
                                />
                              </Grid2>
                              <Grid2 size={6}>
                                <Controller
                                  name="protein"
                                  rules={{ required: true }}
                                  render={({ field }) => (
                                    <TextField
                                      label="Protein"
                                      {...field}
                                      fullWidth
                                      slotProps={{
                                        inputLabel: { shrink: forceShrink },
                                        htmlInput: {
                                          step: '.1',
                                        },
                                      }}
                                      type="number"
                                      size="small"
                                    />
                                  )}
                                />
                              </Grid2>
                              <Grid2 size={6}>
                                <Controller
                                  name="sugar"
                                  rules={{ required: true }}
                                  render={({ field }) => (
                                    <TextField
                                      label="Sugar"
                                      {...field}
                                      fullWidth
                                      slotProps={{
                                        inputLabel: { shrink: forceShrink },
                                        htmlInput: {
                                          step: '.1',
                                        },
                                      }}
                                      type="number"
                                      size="small"
                                    />
                                  )}
                                />
                              </Grid2>
                              <Grid2 size={6}>
                                <Controller
                                  name="fiber"
                                  rules={{ required: true }}
                                  render={({ field }) => (
                                    <TextField
                                      label="Fiber"
                                      {...field}
                                      fullWidth
                                      slotProps={{
                                        inputLabel: { shrink: forceShrink },
                                        htmlInput: {
                                          step: '.1',
                                        },
                                      }}
                                      type="number"
                                      size="small"
                                    />
                                  )}
                                />
                              </Grid2>
                              <Grid2 size={6}>
                                <Controller
                                  name="carbs"
                                  rules={{ required: true }}
                                  render={({ field }) => (
                                    <TextField
                                      label="Carbs"
                                      {...field}
                                      fullWidth
                                      slotProps={{
                                        inputLabel: { shrink: forceShrink },
                                        htmlInput: {
                                          step: '.1',
                                        },
                                      }}
                                      type="number"
                                      size="small"
                                    />
                                  )}
                                />
                              </Grid2>
                              <Grid2 size={6}>
                                <Controller
                                  name="fat"
                                  rules={{ required: true }}
                                  render={({ field }) => (
                                    <TextField
                                      label="Fat"
                                      {...field}
                                      fullWidth
                                      slotProps={{
                                        inputLabel: { shrink: forceShrink },
                                        htmlInput: {
                                          step: '.1',
                                        },
                                      }}
                                      type="number"
                                      size="small"
                                    />
                                  )}
                                />
                              </Grid2>
                              <Grid2 size={6}>
                                <Controller
                                  name="saturatedFat"
                                  rules={{ required: true }}
                                  render={({ field }) => (
                                    <TextField
                                      label="Saturated Fat"
                                      {...field}
                                      fullWidth
                                      slotProps={{
                                        inputLabel: { shrink: forceShrink },
                                        htmlInput: {
                                          step: '.1',
                                        },
                                      }}
                                      type="number"
                                      size="small"
                                    />
                                  )}
                                />
                              </Grid2>
                              <Grid2 size={6}>
                                <Controller
                                  name="sodium"
                                  rules={{ required: true }}
                                  render={({ field }) => (
                                    <TextField
                                      label="Sodium"
                                      {...field}
                                      fullWidth
                                      slotProps={{
                                        inputLabel: { shrink: forceShrink },
                                        htmlInput: {
                                          step: '.1',
                                        },
                                      }}
                                      type="number"
                                      size="small"
                                    />
                                  )}
                                />
                              </Grid2>
                              <Grid2 size={6}>
                                <Controller
                                  name="cholesterol"
                                  rules={{ required: true }}
                                  render={({ field }) => (
                                    <TextField
                                      label="Cholesterol"
                                      {...field}
                                      fullWidth
                                      slotProps={{
                                        inputLabel: { shrink: forceShrink },
                                        htmlInput: {
                                          step: '.1',
                                        },
                                      }}
                                      type="number"
                                      size="small"
                                    />
                                  )}
                                />
                              </Grid2>
                            </Grid2>
                          </TabPanel>
                        </TabContext>
                      </Paper>
                    </Stack>
                  </Grid2>

                  <Grid2
                    container
                    direction="column"
                    sx={{
                      alignItems: 'stretch',
                      justifyContent: 'space-between',
                    }}
                    size={7}
                  >
                    <Grid2
                      container
                      direction="column"
                      sx={{
                        alignItems: 'stretch',
                      }}
                    >
                      <Controller
                        name="name"
                        rules={{ required: true }}
                        render={({ field }) => (
                          <TextField
                            label="Name"
                            {...field}
                            fullWidth
                            slotProps={{
                              inputLabel: { shrink: forceShrink },
                            }}
                          />
                        )}
                      />
                      <Stack
                        direction="column"
                        spacing={1}
                        sx={{
                          justifyContent: 'center',
                          alignItems: 'stretch',
                          minHeight: 142,
                        }}
                      >
                        <Typography
                          variant="h6"
                          gutterBottom={false}
                          textAlign={'left'}
                        >
                          Steps
                        </Typography>
                        {currSteps.map((currStep, index) => (
                          <Box
                            key={index}
                            sx={{
                              px: 2,
                              py: 1,
                              border: '1px solid',
                              borderColor: 'divider',
                              borderRadius: 2,
                              position: 'relative',
                              height: '57px',
                              display: 'flex',
                              alignItems: 'center',
                            }}
                          >
                            <Typography
                              textAlign={'left'}
                              variant="body1"
                              sx={{
                                maxWidth: '400px',
                                overflow: 'hidden',
                                textOverflow: 'ellipsis',
                              }}
                            >
                              {currStep}
                            </Typography>
                            <Grid2
                              sx={{
                                position: 'absolute',
                                right: 0,
                                top: 0,
                                bottom: 0,
                                justifyContent: 'center',
                              }}
                              container
                            >
                              <Dialog
                                open={openStepEdit}
                                onClose={handleCloseEditStepPopup}
                                fullWidth
                              >
                                <DialogTitle
                                  sx={{
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                  }}
                                >
                                  Edit a Step
                                  <IconButton
                                    onClick={handleCloseEditStepPopup}
                                  >
                                    <Close />
                                  </IconButton>
                                </DialogTitle>
                                <DialogContent>
                                  <TextField
                                    label="Edit a Step"
                                    multiline
                                    rows={5}
                                    fullWidth
                                    value={stepToEdit}
                                    onChange={handleStepChangeEditInput}
                                    sx={{ mt: 2 }}
                                  />
                                </DialogContent>
                                <DialogActions>
                                  <Button
                                    variant="outlined"
                                    onClick={(e) => handleStepEdit(index)}
                                  >
                                    Save Step
                                  </Button>
                                </DialogActions>
                              </Dialog>
                              <IconButton
                                sx={{ borderRadius: 0 }}
                                onClick={(e) =>
                                  handleOpenEditStepPopup(null, index)
                                }
                                aria-label={`Edit Step ${index}`}
                              >
                                <Edit />
                              </IconButton>
                              <IconButton
                                sx={{ borderRadius: 0 }}
                                onClick={(e) => handleStepRemove(index)}
                                aria-label={`Delete Step ${index}`}
                              >
                                <DeleteOutline />
                              </IconButton>
                            </Grid2>
                          </Box>
                        ))}
                      </Stack>
                    </Grid2>
                    <Grid2 container sx={{ justifyContent: 'space-between' }}>
                      <Popover
                        open={openStepAdd}
                        anchorEl={anchorEl}
                        onClose={handleCloseAddStepPopup}
                        anchorOrigin={{
                          vertical: 'top',
                          horizontal: 'left',
                        }}
                        transformOrigin={{
                          vertical: 'bottom',
                          horizontal: 'left',
                        }}
                      >
                        <Grid2
                          container
                          spacing={2}
                          sx={{
                            my: 2,
                            mx: 5,
                            justifyContent: 'flex-end',
                            width: '565px',
                          }}
                        >
                          <Grid2 size={12}>
                            <TextField
                              label="Add a Step"
                              multiline
                              rows={5}
                              fullWidth
                              value={stepToAdd}
                              onChange={handleStepChangeAddInput}
                            />
                          </Grid2>

                          <Button variant="outlined" onClick={handleStepAdd}>
                            Add Step
                          </Button>
                        </Grid2>
                      </Popover>
                      <Grid2 size={12}>
                        <TablePagination
                          component="div"
                          count={steps.length}
                          page={stepPage}
                          onPageChange={handleStepChangePage}
                          rowsPerPage={5}
                          rowsPerPageOptions={[]}
                        />
                      </Grid2>
                      <IconButton
                        onClick={handleOpenAddStepPopup}
                        aria-label="Add New Step"
                      >
                        <AddCircleOutline color="primary" />
                      </IconButton>
                      <Button type="submit" variant="contained">
                        Submit
                      </Button>
                    </Grid2>
                  </Grid2>
                </Grid2>
              </Box>
            </FormProvider>
          </Paper>
        </>
      )}
    </Container>
  )
}

export default RecipeForm
