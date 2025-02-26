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
import { FavoriteRequest, Post, Recipe, RecipeListData } from '../../api/types'
import {
  ThumbDownOutlined,
  ThumbUp,
  Star,
  Edit,
  Favorite,
  FavoriteBorder,
} from '@mui/icons-material'
import { useTheme } from '../../Themes/themeContext'
import { useNavigate } from 'react-router-dom'
import {
  useCheckUserFavoritesQuery,
  useFavoriteRecipeMutation,
  useUnfavoriteRecipeMutation,
} from '../UserRecipes/UserRecipeSlice'
import { useAuth } from '../Authentication/AuthProvider'
import { useEffect } from 'react'

interface RecipeListItemProp {
  recipe: RecipeListData
  index: number
}

const RecipeListItem = (props: RecipeListItemProp) => {
  const { theme } = useTheme()
  const auth = useAuth()
  const navigateTo = useNavigate()
  const index = props.index
  const recipe = props.recipe

  const { data: favorited, isLoading: favoriteLoading } =
    useCheckUserFavoritesQuery(
      {
        userId: auth?.user.id ?? -1,
        recipeId: props.recipe.recipeId,
      },
      { skip: !auth }
    )

  useEffect(() => {
    // console.log('favorited', favorited)
  }, [favorited])

  const [favoriteRecipe] = useFavoriteRecipeMutation()
  const [unfavoriteRecipe] = useUnfavoriteRecipeMutation()

  const gotoRecipe = () => {
    navigateTo('/recipe-details/' + recipe.recipeId)
  }

  const goToEditRecipe = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.stopPropagation()
    navigateTo('/edit-recipe/' + recipe.recipeId)
  }

  const handleToggleFavorite = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.stopPropagation()

    if (favoriteLoading || !auth) return

    let req: FavoriteRequest = {
      userId: auth.user.id,
      recipeId: props.recipe.recipeId,
    }

    console.log(props.recipe.recipeId)
    if (favorited) {
      unfavoriteRecipe(req)
    } else {
      favoriteRecipe(req)
    }
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
          <Grid2 container columns={24}>
            <Grid2 size={23}>
              <Typography
                sx={{ textAlign: 'left', color: theme.color }} // Theme color for text
                variant="subtitle2"
              >
                Prep Time : {recipe.prepTime} | Cook Time : {recipe.cookTime}
              </Typography>
            </Grid2>
            <Grid2 size={1}>
              <IconButton onClick={goToEditRecipe}>
                <Edit />
              </IconButton>
            </Grid2>

            <Grid2 size={23}>
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
            </Grid2>
            <Grid2 size={1}>
              <IconButton onClick={handleToggleFavorite}>
                {favorited ? <Favorite /> : <FavoriteBorder />}
              </IconButton>
            </Grid2>
          </Grid2>
        </CardContent>
      </CardActionArea>
    </Card>
  )
}

export default RecipeListItem
