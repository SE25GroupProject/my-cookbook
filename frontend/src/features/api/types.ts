export interface User {
  id: number
  username: string
  password: string
}

export type UserCred = Pick<User, 'username' | 'password'>
export type UserInfo = Pick<User, 'id' | 'username'>

export interface Recipe {
  id: number
  name: string
  cookTime: string
  prepTime: string
  totalTime: string
  description: string
  images: string[]
  category: string
  tags: string[]
  ingredientQuantities: string[]
  ingredients: string[]
  rating: number
  calories: number
  fat: number
  saturatedFat: number
  cholesterol: number
  sodium: number
  carbs: number
  fiber: number
  sugar: number
  protein: number
  servings: number
  instructions: string[]
}

export class RecipeObject implements Recipe {
  id!: number
  name!: string
  cookTime!: string
  prepTime!: string
  totalTime!: string
  description!: string
  images!: string[]
  category!: string
  tags!: string[]
  ingredientQuantities!: string[]
  ingredients!: string[]
  rating!: number
  calories!: number
  fat!: number
  saturatedFat!: number
  cholesterol!: number
  sodium!: number
  carbs!: number
  fiber!: number
  sugar!: number
  protein!: number
  servings!: number
  instructions!: string[]
}
export interface NutritionMax {
  caloriesUp: number
  fatUp: number
  sugUp: number
  proUp: number
}

export interface RecipeListIngredientsRequest {
  ingredients: String[]
  page: number
}

export interface RecipeListNutritionRequest {
  caloriesUp: number
  fatUp: number
  sugUp: number
  proUp: number
  page: number
}

export interface RecipeListResponse {
  recipes: Recipe[]
  count: number
  page: number
}

/**
 * A slice of a recipe that only includes the recipes id and name
 *
 * @typedef PostRecipe
 * @property {number} [text="id"] The id associated with the recipe.
 */
export type PostRecipe = Pick<Recipe, 'id' | 'name'>

export interface PostComment {
  content: string
  liked: boolean
  disliked: boolean
}

/**
 * A Post object that stores a message, image, and recipe added by a user.
 *
 * @typedef Post
 * @property {PostRecipe} recipe The recipe information associated with a post.
 * @property {string} img The image information that can be used to display and store the image.
 */
export interface Post {
  recipe: PostRecipe
  img: string
  content: string
  liked: boolean
  disliked: boolean
  comments: PostComment[]
}

export type RecipeListData = Pick<
  Recipe,
  | 'id'
  | 'name'
  | 'description'
  | 'cookTime'
  | 'prepTime'
  | 'category'
  | 'rating'
>
