import internal from 'stream'

export interface User {
  id: number
  username: string
  password: string
}

export type UserCred = Pick<User, 'username' | 'password'>
export type UserInfo = Pick<User, 'id' | 'username'>

export interface Instruction {
  step: number
  instruction: string
}

export interface Recipe {
  recipeId: number
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
  instructions: Instruction[]
}

export class RecipeObject implements Recipe {
  recipeId!: number
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
  instructions!: Instruction[]
}

export type UserRecipe = Partial<Recipe> & {
  userId: number
}

export interface NutritionMax {
  caloriesMax: number
  fatMax: number
  sugMax: number
  proMax: number
}

export interface RecipeListIngredientsRequest {
  ingredients: String[]
  page: number
}

export interface RecipeListNutritionRequest {
  caloriesMax: number
  fatMax: number
  sugMax: number
  proMax: number
  page: number
}

export interface RecipeListResponse {
  recipes: Recipe[]
  count: number
  page: number
}

export type RecipeListData = Pick<
  Recipe,
  | 'recipeId'
  | 'name'
  | 'description'
  | 'cookTime'
  | 'prepTime'
  | 'category'
  | 'rating'
>

/**
 * A slice of a recipe that only includes the recipes id and name
 *
 * @typedef PostRecipe
 * @property {number} [text="id"] The id associated with the recipe.
 */
export type PostRecipe = Pick<Recipe, 'recipeId' | 'name'>

export interface PostComment {
  commentId: number
  postId: number
  userId: number
  message: string
}

export type PostCommentRequest = Pick<
  PostComment,
  'postId' | 'userId' | 'message'
>

/**
 * A Post object that stores a message, image, and recipe added by a user.
 *
 * @typedef Post
 * @property {PostRecipe} recipe The recipe information associated with a post.
 * @property {string} img The image information that can be used to display and store the image.
 */
export interface Post {
  postId: number
  userId: number
  recipe: PostRecipe
  image: string
  message: string
  likes: number[]
  dislikes: number[]
  comments: PostComment[]
}

export type PostRequest = Pick<
  Post,
  'postId' | 'userId' | 'image' | 'message' | 'recipe'
>

export type PostUpdate = Pick<Post, 'postId' | 'userId'>

export interface ShoppingItem {
  name: string
  quantity: number
  unit: string
  checked: boolean
}

export type ShoppingItemRequest = ShoppingItem & {
  userId: number
}

export interface MealPlanEntry {
  day: number
  recipe: PostRecipe
}

export type MealPlanUpdate = MealPlanEntry & {
  userId: number
}

export interface MealPlanDelete {
  day: number
  userId: number
}

export interface FavoriteRequest {
  userId: number
  recipeId: number
}
