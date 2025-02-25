/*

Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com

*/

/**
 * File name: RecipeInformation.tsx
 * Task - This component displays images for recipe making, the procedure to make the dish and the
 * trivia and factual info related to it.
 * This component is a dynamic component and is seen only when you click on a recipe from the recipe list
 * @author Priyanka Ambawane - dearpriyankasa@gmail.com
 */
import {
  IconButton,
  Grid2,
  Paper,
  Stack,
  Typography,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  CircularProgress,
} from '@mui/material'
import StarIcon from '@mui/icons-material/Star'
import React, { useEffect, useState } from 'react'
import { Provider } from 'react-redux'
import applicationStore from '../../../store'
import { useDispatch, useSelector } from 'react-redux'
import { useParams } from 'react-router-dom'
import './RecipeInformation.css'
import noImage from './no-image.png'
import axios from 'axios'
import { useTheme } from '../../Themes/themeContext'
import { useNavigate } from 'react-router-dom'
import { useGetRecipeQuery } from './RecipeInfoSlice'
import { Instruction, Recipe, RecipeObject } from '../../api/types'

import SvgIcon, { SvgIconProps } from '@mui/material/SvgIcon'
import { WhatsApp } from '@mui/icons-material'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {
  faDiscord,
  faSlack,
  faWhatsapp,
} from '@fortawesome/free-brands-svg-icons'
import { useUpdateMealPlanMutation } from '../MealPlan/MealPlanSlice'
import { useAuth } from '../Authentication/AuthProvider'

const store = applicationStore()

const shareOnWhatsApp = (recipeUrl: string) => {
  const baseUrl =
    process.env.NODE_ENV === 'production'
      ? process.env.REACT_APP_WHATSAPP_URL_PROD ||
        'https://api.whatsapp.com/send?text='
      : process.env.REACT_APP_WHATSAPP_URL_TEST ||
        'https://api.whatsapp.com/send?text='

  const whatsappUrl = `${baseUrl}Check out this recipe: ${encodeURIComponent(
    recipeUrl
  )}`
  window.open(whatsappUrl, '_blank')
  // const whatsappUrl = `https://api.whatsapp.com/send?text=Check out this recipe: ${encodeURIComponent(recipeUrl)}`;
}

const shareOnPlatform = (recipeUrl: string, platform: 'slack' | 'discord') => {
  const baseUrls = {
    slack:
      process.env.NODE_ENV === 'production'
        ? process.env.REACT_APP_SLACK_URL_PROD ||
          'https://slack.com/intl/en-us/share?text='
        : process.env.REACT_APP_SLACK_URL_TEST ||
          'https://slack.com/intl/en-us/share?text=',
    discord: 'https://discord.com/channels/@me?message=',
  }

  const encodedRecipe = encodeURIComponent(recipeUrl)
  const shareUrl =
    platform === 'slack'
      ? `${baseUrls.slack}Check out this recipe: ${encodedRecipe}`
      : `${baseUrls.discord}Check out this recipe: ${encodedRecipe}`

  window.open(shareUrl, '_blank')
}

const CopyUrlModal = ({ open, onClose, url, platform }: any) => {
  const handleCopy = () => {
    navigator.clipboard?.writeText(url)
    onClose()
    shareOnPlatform(url, platform)
  }

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
      data-testid="CopyModal"
    >
      <DialogTitle>Copy URL</DialogTitle>
      <DialogContent>
        <TextField
          fullWidth
          value={url}
          variant="outlined"
          // inputProps={{ readOnly: true }}
          multiline
          rows={2}
          style={{ wordWrap: 'break-word', height: 'auto' }}
        />
        <Typography
          variant="body2"
          color="textSecondary"
          style={{ marginTop: 10 }}
        >
          Click the "COPY" button to copy the URL. Then, Paste it into the
          message box on selected platform.
        </Typography>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCopy} color="primary">
          Copy
        </Button>
      </DialogActions>
    </Dialog>
  )
}

const RecipeInformationWrapped = () => {
  const { theme } = useTheme()
  const auth = useAuth()
  const navigate = useNavigate() // For redirecting to Meal Plan page
  let { id } = useParams()
  const dispatch = useDispatch()
  const [input, setInput] = useState('')
  const [response, setResponse] = useState('')
  const [showInput, setShowInput] = useState(false)
  const [openModal, setOpenModal] = useState<boolean>(false)
  const [selectedPlatform, setSelectedPlatform] = useState('slack')
  const [selectedDayIndex, setSelectedDayIndex] = useState(0)
  const [addToMealPlan] = useUpdateMealPlanMutation()

  const { data: recipe, isLoading, isSuccess } = useGetRecipeQuery(id as string)
  console.log(recipe)
  let images = recipe?.images ? [...recipe?.images] : []

  let triviaPaperStyles = {
    background: theme.background,
    marginTop: '20px',
    padding: '20px',
    marginLeft: '30px',
    marginRight: '30px',
  }

  const handleShareClick = (urlId: string, platform: 'slack' | 'discord') => {
    setOpenModal(true)
    setSelectedPlatform(platform)
  }

  const handleButtonClick = () => {
    setShowInput(true)
  }

  const handleInputChange = (e: any) => {
    setInput(e.target.value)
  }

  // accesses the state of the component from the app's store
  // const recipeInfo = useSelector((state: any) => state.getRecipeInfoAppState)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [availableVoices, setAvailableVoices] = useState<
    SpeechSynthesisVoice[]
  >([])
  const [selectedVoice, setSelectedVoice] =
    useState<SpeechSynthesisVoice | null>(null)

  useEffect(() => {
    // Load available voices
    const loadVoices = () => {
      if (window.speechSynthesis) {
        const voices = window.speechSynthesis.getVoices()
        setAvailableVoices(voices)
        if (voices.length > 0) {
          setSelectedVoice(voices[0]) // Default to the first voice
        }
      }
    }

    // Ensure voices are loaded
    loadVoices()
    if (window.speechSynthesis) {
      if (typeof window.speechSynthesis.onvoiceschanged !== 'undefined') {
        window.speechSynthesis.onvoiceschanged = loadVoices
      }
    }
  }, [])

  const speakInstructions = (instruction: string) => {
    if (!isSpeaking && selectedVoice) {
      const synth = window.speechSynthesis
      const utterance = new SpeechSynthesisUtterance(instruction)
      utterance.voice = selectedVoice
      utterance.onend = () => setIsSpeaking(false)
      synth.speak(utterance)
      setIsSpeaking(true)
    }
  }
  /* the effect hook below does an api call to get the recipe details
      using the recipe id as soon as the compnent gets loaded up */
  // useEffect(() => {
  //   // dispatch(getRecipeInfoInitiator('http://localhost:8000/recipe/' + id))
  //   return () => {
  //     // state cleanup here
  //   }
  // }, [])

  if (isLoading) {
    return (
      <div data-testid="RecipeInfoLoading">
        <CircularProgress />
        Loading...
      </div>
    )
  } else if (isSuccess) {
    // const recipe = recipeInfo.getRecipeInfoData // The recipe object containing all necessary information
    const instructionArr = recipe.instructions.map((inst) => inst.instruction)

    const recipeDetailsforLLM = `
      Name: ${recipe.name}
      Ingredients: ${recipe.ingredients ? recipe.ingredients.join(', ') : []}
      Rating: ${recipe.rating}
      Prep Time: ${recipe.prepTime}
      Sugar: ${recipe.sugar}g
      Carbs: ${recipe.carbs}g
      Protein: ${recipe.protein}g
      Cuisine: ${recipe.category}
      Servings: ${recipe.servings}
      Cook Time: ${recipe.cookTime}
      Cholesterol: ${recipe.cholesterol}mg/dl
      Fat: ${recipe.fat}g
      Instructions: ${instructionArr ? instructionArr.join(' ') : []}
    `
    const handleSubmit = async () => {
      try {
        const result = await axios.post(
          'http://localhost:8000/recipe/recommend-recipes/',
          { query: input, context: recipeDetailsforLLM }
        )
        setResponse(result.data.response)
      } catch (error) {
        console.error('Error fetching recipe recommendations:', error)
      }
    }
    // Function to handle formatting
    const formatText = (text: string) => {
      return text.split('\n').map((line, index) => {
        // Check for "**" bold markers first
        const boldRegex = /\*\*(.*?)\*\*/g
        let formattedLine = line
        if (boldRegex.test(line)) {
          // Replace "**text**" with <strong>text</strong>
          formattedLine = line.replace(
            boldRegex,
            (match, p1) => `<strong>${p1}</strong>`
          )
        }

        // Check if the line starts with "*", convert to list items
        if (formattedLine.trim().startsWith('*')) {
          return <li key={index}>{formattedLine.replace('*', '').trim()}</li>
        }

        // Return as a paragraph for other lines
        return (
          <p
            key={index}
            dangerouslySetInnerHTML={{ __html: formattedLine }}
          ></p>
        )
      })
    }

    const handleAddToMealPlan = async (
      recipeToAdd: Recipe,
      dayIndex: number
    ) => {
      if (!auth) return

      addToMealPlan({
        day: dayIndex,
        userId: auth?.user.id,
        recipe: recipeToAdd,
      })
        .unwrap()
        .then((mealPlanResponse) => {
          console.log(mealPlanResponse)
          alert(
            `${recipeToAdd.name} added to the meal plan for ${
              [
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday',
                'Sunday',
              ][dayIndex]
            }!`
          )
        })
        .catch((err) => {
          console.error('Error saving meal plan:', err)

          alert('Failed to save the meal plan. Please try again.')
        })
    }

    return (
      <div
        style={{
          width: '100vw',
          color: theme.color,
          paddingTop: '20px',
          background: theme.background,
        }}
        data-testid="RecipeInfo"
      >
        {openModal && (
          <CopyUrlModal
            open={openModal}
            onClose={() => setOpenModal(false)}
            url={`https://cookbook-alpha.vercel.app/recipe-details/${id}`}
            platform={selectedPlatform}
          />
        )}
        <Typography variant="h4" gutterBottom className="recipe-header">
          {recipe.name}
        </Typography>
        <div style={{ marginTop: '10px' }}>
          <select
            style={{
              backgroundColor: theme.headerColor,
              color: theme.color,
              border: `1px solid ${theme.headerColor}`,
              borderRadius: '4px',
              padding: '8px 12px',
              marginRight: '10px',
              fontSize: '16px',
              transition:
                'transform 0.2s ease, background-color 0.2s ease, border-color 0.2s ease',
              cursor: 'pointer',
            }}
            onChange={(e) => setSelectedDayIndex(Number(e.target.value))}
            value={selectedDayIndex}
          >
            {[
              'Monday',
              'Tuesday',
              'Wednesday',
              'Thursday',
              'Friday',
              'Saturday',
              'Sunday',
            ].map((day, index) => (
              <option
                key={index}
                value={index}
                style={{
                  backgroundColor: theme.background,
                  color: theme.color,
                  fontSize: '16px',
                }}
              >
                {day}
              </option>
            ))}
          </select>
          <Button
            variant="contained"
            style={{
              backgroundColor: theme.headerColor,
              color: theme.color,
              marginRight: '10px',
              transition: 'transform 0.2s ease, background-color 0.2s ease',
            }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.backgroundColor = theme.background)
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.backgroundColor = theme.headerColor)
            }
            onClick={() => handleAddToMealPlan(recipe, selectedDayIndex)}
          >
            Add to Meal Plan
          </Button>
          <Button
            variant="outlined"
            style={{
              borderColor: theme.headerColor,
              color: theme.headerColor,
              transition: 'transform 0.2s ease, border-color 0.2s ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.color = theme.color
              e.currentTarget.style.borderColor = theme.color
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.color = theme.headerColor
              e.currentTarget.style.borderColor = theme.headerColor
            }}
            onClick={() => navigate('/meal')}
          >
            Go to Meal Plan
          </Button>
        </div>

        <div
          style={{
            float: 'left',
            width: '30vw',
            color: theme.color,
            background: theme.background,
          }}
        >
          <Paper elevation={24} style={triviaPaperStyles}>
            <Grid2
              container
              spacing={3}
              style={{ background: theme.background, color: theme.color }}
            >
              <Grid2
                size={{ xs: 12 }}
                style={{
                  textAlign: 'center',
                  color: theme.color,
                  background: theme.background,
                }}
              >
                <Typography variant="h5" gutterBottom>
                  Summary
                </Typography>
              </Grid2>
              <Grid2
                size={{ xs: 12 }}
                textAlign={'left'}
                style={{ background: theme.background, color: theme.color }}
              >
                <Typography variant="h6">Ingredients:</Typography>
                <Typography variant="subtitle1" gutterBottom>
                  {recipe?.ingredients?.map((ele: any, idx: number) => {
                    return (
                      <span key={idx}>
                        {idx > 0 && ', '}
                        {ele}
                      </span>
                    )
                  })}
                </Typography>
              </Grid2>
              <Grid2 size={{ xs: 6 }}>
                <Stack
                  direction="column"
                  spacing={2}
                  paddingBottom="20px"
                  textAlign={'left'}
                >
                  <Typography variant="h6">
                    Rating:
                    <Typography variant="body1" gutterBottom>
                      {Array.from({
                        length: Math.floor(Number(recipe?.rating)),
                      }).map((ele: any, idx: number) => {
                        return <StarIcon key={idx} fontSize="small" />
                      })}
                    </Typography>
                  </Typography>
                  <Typography variant="h6">
                    Prep Time:
                    <Typography variant="body1" gutterBottom>
                      {recipe?.prepTime}
                    </Typography>
                  </Typography>
                  <Typography variant="h6">
                    Sugar:
                    <Typography variant="body1" gutterBottom>
                      {recipe?.sugar}g
                    </Typography>
                  </Typography>
                  <Typography variant="h6">
                    Carbs:
                    <Typography variant="body1" gutterBottom>
                      {recipe?.carbs}g
                    </Typography>
                  </Typography>
                  <Typography variant="h6">
                    Proteins:
                    <Typography variant="body1" gutterBottom>
                      {recipe?.protein}g
                    </Typography>
                  </Typography>
                </Stack>
              </Grid2>
              <Grid2 size={{ xs: 6 }}>
                <Stack
                  direction="column"
                  spacing={2}
                  paddingBottom="20px"
                  textAlign={'left'}
                >
                  <Typography variant="h6">
                    Cuisine:
                    <Typography variant="body1" gutterBottom>
                      {recipe?.category}
                    </Typography>
                  </Typography>
                  <Typography variant="h6">
                    Servings:
                    <Typography variant="body1" gutterBottom>
                      {recipe?.servings}
                    </Typography>
                  </Typography>
                  <Typography variant="h6">
                    Cook Time:
                    <Typography variant="body1" gutterBottom>
                      {recipe?.cookTime}
                    </Typography>
                  </Typography>
                  <Typography variant="h6">
                    Cholestrol:
                    <Typography variant="body1" gutterBottom>
                      {recipe?.cholesterol}mg/dl
                    </Typography>
                  </Typography>
                  <Typography variant="h6">
                    Fats:
                    <Typography variant="body1" gutterBottom>
                      {recipe?.fat}g
                    </Typography>
                  </Typography>
                </Stack>
              </Grid2>
              <Grid2
                size={{ xs: 12 }}
                style={{
                  marginTop: '20px',
                  display: 'flex',
                  justifyContent: 'space-between',
                }}
              >
                <button
                  onClick={() => shareOnWhatsApp(window.location.href)} // Generates a WhatsApp sharing link for the recipe
                  style={{
                    backgroundColor: '#25D366',
                    color: 'white',
                    padding: '10px 20px',
                    border: 'none',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)',
                    transition: 'transform 0.2s ease',
                  }}
                  onMouseEnter={(e) =>
                    (e.currentTarget.style.transform = 'scale(1.05)')
                  }
                  onMouseLeave={(e) =>
                    (e.currentTarget.style.transform = 'scale(1)')
                  }
                >
                  {/* <FaWhatsapp
                    style={{ marginRight: '10px', fontSize: '1.2em' }}
                  /> */}
                  <FontAwesomeIcon icon={faWhatsapp} />
                  WhatsApp
                </button>
                <button
                  onClick={() =>
                    handleShareClick(window.location.href, 'slack')
                  }
                  style={{
                    backgroundColor: '#7C3085',
                    color: 'white',
                    padding: '10px 20px',
                    border: 'none',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)',
                    transition: 'transform 0.2s ease',
                  }}
                  onMouseEnter={(e) =>
                    (e.currentTarget.style.transform = 'scale(1.05)')
                  }
                  onMouseLeave={(e) =>
                    (e.currentTarget.style.transform = 'scale(1)')
                  }
                >
                  {/* <FaSlack style={{ marginRight: '10px', fontSize: '1.2em' }} /> */}
                  <FontAwesomeIcon icon={faSlack} />
                  Slack
                </button>
                <button
                  onClick={() =>
                    handleShareClick(window.location.href, 'discord')
                  }
                  style={{
                    backgroundColor: '#5865F2',
                    color: 'white',
                    padding: '10px 20px',
                    border: 'none',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)',
                    transition: 'transform 0.2s ease',
                  }}
                  onMouseEnter={(e) =>
                    (e.currentTarget.style.transform = 'scale(1.05)')
                  }
                  onMouseLeave={(e) =>
                    (e.currentTarget.style.transform = 'scale(1)')
                  }
                >
                  <FontAwesomeIcon icon={faDiscord} />
                  Discord
                </button>
              </Grid2>
            </Grid2>
          </Paper>
        </div>
        <div style={{ float: 'left', width: '40vw', marginTop: '15px' }}>
          <Grid2 container spacing={3}>
            <Grid2 size={{ xs: 12 }}>
              <Stack
                direction="column"
                spacing={2}
                paddingBottom="20px"
                textAlign={'left'}
              >
                <div className="helper-text" style={{ color: theme.color }}>
                  Tap on any step below to hear the instructions read aloud.
                  Follow along with the recipe as you cook, and feel free to
                  pause or repeat any step!
                </div>
                <div style={{ marginBottom: '20px' }}>
                  <label
                    htmlFor="voiceSelector"
                    style={{ marginRight: '10px' }}
                  >
                    Select Voice:
                  </label>
                  <select
                    id="voiceSelector"
                    style={{
                      backgroundColor: theme.headerColor,
                      color: theme.color,
                      borderColor: theme.color,
                      padding: '10px 20px',
                      borderRadius: '5px',
                      boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)',
                      transition:
                        'transform 0.2s ease, background-color 0.2s ease, border-color 0.2s ease',
                      cursor: 'pointer',
                    }}
                    onChange={(e) => {
                      const selected = availableVoices.find(
                        (voice) => voice.name === e.target.value
                      )
                      setSelectedVoice(selected || null)
                    }}
                    value={selectedVoice?.name || ''}
                  >
                    {availableVoices.map((voice) => (
                      <option key={voice.name} value={voice.name}>
                        {voice.name} ({voice.lang})
                      </option>
                    ))}
                  </select>
                </div>
                {recipe?.instructions?.map((inst: Instruction, idx: number) => (
                  <div
                    style={{
                      backgroundColor: theme.background, // Card background from theme
                      color: theme.color, // Card text color
                      borderColor: theme.headerColor,
                      borderWidth: '2px', // Set the desired border thickness
                      borderStyle: 'solid',
                    }}
                    key={idx}
                    className="step"
                    onClick={() => speakInstructions(inst.instruction)}
                  >
                    <Typography variant="h6">
                      Step {inst.step}:
                      <Typography variant="body1" gutterBottom>
                        {inst.instruction}
                      </Typography>
                    </Typography>
                  </div>
                ))}
              </Stack>
              <Stack
                direction="column"
                spacing={2}
                paddingBottom="20px"
                textAlign={'left'}
              >
                <Button
                  onClick={handleButtonClick}
                  variant="contained"
                  color="primary"
                  style={{
                    width: '200px',
                    color: theme.color,
                    background: theme.headerColor,
                  }}
                >
                  CUSTOMIZE
                </Button>
                {showInput && (
                  <div
                    className="input-group"
                    style={{
                      backgroundColor: theme.headerColor, // Card background from theme
                      color: theme.color, // Card text color
                    }}
                  >
                    <label htmlFor="ai-input" id="ai-input"></label>
                    <input
                      type="text"
                      value={input}
                      onChange={handleInputChange}
                      className="input-textbox"
                      id="ai-input"
                      placeholder="Type your customization..."
                    />
                    {input.length > 0 && (
                      <button
                        onClick={handleSubmit}
                        className="submit-button"
                        id="ai-submit"
                        data-testid="ai-submit"
                      ></button>
                    )}
                  </div>
                )}
                <Typography variant="subtitle1" gutterBottom>
                  {formatText(response)}
                </Typography>
              </Stack>
            </Grid2>
          </Grid2>
        </div>
        <div
          style={{
            float: 'left',
            width: '30vw',
            color: theme.color,
            background: theme.headerColor,
          }}
        >
          {images && images[0] !== '' ? (
            <Typography variant="subtitle1" gutterBottom>
              <Stack direction="column" spacing={2} padding="25px">
                {images
                  .reverse()
                  .slice(0, 3)
                  .map((imageLink: string, idx: number) => {
                    imageLink = imageLink.replaceAll('"', '')
                    return (
                      <img
                        src={imageLink}
                        alt={`Cannot display pic ${idx + 1}`}
                        key={idx}
                      />
                    )
                  })}
              </Stack>
            </Typography>
          ) : (
            <img src={noImage} alt={`Cannot display pic`} />
          )}
        </div>
      </div>
    )
  } else {
    return <> Error! Recipe not found! </>
  }
}

const RecipeInformation = () => {
  return (
    <Provider store={store}>
      <RecipeInformationWrapped />
    </Provider>
  )
}

export default RecipeInformation
