import {
  Button,
  Card,
  CardActionArea,
  CardContent,
  Divider,
  Grid2,
  IconButton,
  Paper,
  Typography,
} from '@mui/material'
import { Post, Recipe, RecipeListData } from '../../api/types'
import { ThumbDownOutlined, ThumbUp, Star } from '@mui/icons-material'
import { useTheme } from '../../Themes/themeContext'
import { useNavigate } from 'react-router-dom'

interface RecipeListItemProp {
  recipe: RecipeListData
  index: number
}

const RecipeListItem = (props: RecipeListItemProp) => {
  const { theme } = useTheme()
  const navigateTo = useNavigate()
  const index = props.index
  const recipe = props.recipe

  const gotoRecipe = () => {
    navigateTo('/recipe-details/' + recipe.recipeId)
  }

  return (
    <Card
      variant="outlined"
      sx={{
        width: 4 / 5,
        my: 1,
        backgroundColor: theme.background, // Card background from theme
        color: theme.color, // Card text color
        borderColor: theme.headerColor,
        borderWidth: '2px', // Set the desired border thickness
        borderStyle: 'solid', // Ensure the border style is solid
        overflow: 'visible',
      }}
      key={index}
    >
      <CardActionArea onClick={() => gotoRecipe()}>
        <CardContent>
          <div className="d-flex flex-row">
            <Typography
              sx={{ fontWeight: 600, color: theme.color }} // Theme color for text
              gutterBottom
              variant="h5"
              component="div"
            >
              {recipe.name} |{' '}
              <Star
                sx={{ color: '#dede04' }} // Star icon color
                fontSize="medium"
              />{' '}
              {recipe.rating}/5.0
            </Typography>
            <Typography
              gutterBottom
              variant="h6"
              component="span"
              className="supplemental-info"
              sx={{ color: theme.color }} // Theme color for text
            >
              {recipe.category}
            </Typography>
          </div>
          <Typography
            sx={{ textAlign: 'left', color: theme.color }} // Theme color for text
            variant="subtitle2"
          >
            Prep Time : {recipe.prepTime} | Cook Time : {recipe.cookTime}
          </Typography>

          <Typography
            sx={{
              textAlign: 'left',
              marginTop: 2,
              fontStyle: 'italic',
              color: theme.color, // Theme color for text
            }}
            variant="body2"
          >
            {recipe.description}
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  )
}

export default RecipeListItem
