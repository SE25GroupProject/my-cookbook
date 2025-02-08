export interface User {
  id: number
  name: string
  password: string
}

type UserCred = Pick<User, 'name' | 'password'>
type UserInfo = Pick<User, 'id' | 'name'>

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
  instruction: string[]
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
  instruction!: string[]
}
export interface NutritionMax {
  caloriesUp: number
  fatUp: number
  sugerUp: number
  proUp: number
}

export interface RecipeListIngredientsRequest {
  ingredients: String[]
  page: number
}

export interface RecipeListNutritionRequest {
  caloriesUp: number
  fatUp: number
  sugerUp: number
  proUp: number
  page: number
}

export interface RecipeListResponse {
  recipes: Recipe[]
  count: number
  page: number
}
