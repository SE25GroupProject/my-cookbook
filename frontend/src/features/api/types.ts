export interface User {
  id: number
  username: string
  password: string
}

export type UserCred = Pick<User, 'username' | 'password'>
export type UserInfo = Pick<User, 'id' | 'username'>

export interface Recipe {
  id: string | number
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
  id!: string | number
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
