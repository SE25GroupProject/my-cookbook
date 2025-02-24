import { Post, PostRecipe, Recipe } from '../api/types'

export const mockRecipe: Recipe = {
  id: 20919,
  name: 'California Scampi',
  cookTime: '5M',
  prepTime: '10M',
  totalTime: '15M',
  description: 'Make and share this California Scampi recipe from Food.com.',
  images: [
    '"https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/20/91/9/picPCmubd.jpg"',
  ],
  category: 'Lobster',
  tags: ['Very Low Carbs', 'Healthy', '< 15 Mins', 'Stove Top'],
  ingredientQuantities: ['1', '1', '2', '3', '1/4', '1/4', '1/4', '1', 'NA")'],
  ingredients: [
    'shrimp',
    'lobster',
    'butter',
    'olive oil',
    'garlic cloves',
    'Italian parsley',
    'white wine',
    'lemon',
  ],
  rating: 5,
  calories: 106.8,
  fat: 3,
  saturatedFat: 0.8,
  cholesterol: 148.9,
  sodium: 175.9,
  carbs: 1.6,
  fiber: 0.1,
  sugar: 0.3,
  protein: 16,
  servings: 6,
  instructions: [
    'Melt butter and oil together in sauté pan.',
    'Add garlic, sauté for one minute, and add shrimp.',
    'Sauté for one minute, add wine, lemon juice, salt, and pepper.',
    'Sauté quickly while sauce reduces and shrimp turns pink.',
    'Do not overcook.',
    'Sprinkle with parsley before serving.',
    'Serve with sauce over noodles or rice.',
    'Garnish with lemon wedges.',
  ],
}

export const mockRecipeTwo: Recipe = {
  id: 58,
  name: 'Low-Fat Burgundy Beef & Vegetable Stew',
  cookTime: '2H14M',
  prepTime: '30M',
  totalTime: '2H44M',
  description:
    'Make and share this Low-Fat Burgundy Beef & Vegetable Stew recipe from Food.com.',
  images: [
    'https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/58/picnE8qoe.jpg',
    'https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/58/picwiayaY.jpg',
    'https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/58/picAaGXgc.jpg',
    'https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/58/picD2ey4Z.jpg',
    'https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/58/picKtSTwb.jpg',
    'https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/58/picY2Aqui.jpg',
  ],
  category: 'Stew',
  tags: [
    'Vegetable',
    'Meat',
    'Low Cholesterol',
    'Healthy',
    'Free Of...',
    'Weeknight',
    '< 4 Hours',
  ],
  ingredientQuantities: [
    '1 1/2',
    '1',
    '1',
    '1/2',
    '1/2',
    '1',
    '1/2',
    '3',
    '5 1/2',
    '1',
    '2',
    '1',
  ],
  ingredients: [
    'beef eye round',
    'dried thyme leaves',
    'salt',
    'pepper',
    'ready-to-serve beef broth',
    'Burgundy wine',
    'garlic',
    'cornstarch',
    'frozen sugar snap peas',
  ],
  rating: 4.5,
  calories: 280.1,
  fat: 6,
  saturatedFat: 1.5,
  cholesterol: 66.9,
  sodium: 591.5,
  carbs: 22.4,
  fiber: 6.1,
  sugar: 9.2,
  protein: 29.8,
  servings: 6,
  instructions: [
    'Trim fat from beef, cut into 1-inch pieces.',
    'In Dutch oven, heat oil over medium high hunt until hot. Add beef (half at a time) and brown evenly, stirring occasionally.',
    'Pour off drippings.',
    'Season with thyme, salt and pepper.',
    'Stir in broth, wine and garlic. Bring to boil; reduce heat to low.',
    'Cover tightly and simmer 1 1/2 hours.',
    'Add carrots and onions.',
    'Cover and continue cooking 35 to 40 minutes or until beef and vegetables are tender.',
    'Bring beef stew to a boil over medium-high heat. Add cornstarch mixture; cook and stir 1 minute. Stir in sugar snap peas.',
    'Reduce heat to medium and cook 3 to 4 minutes or until peas are heated through.',
  ],
}

export const testPosts: Post[] = [
  {
    recipe: { id: 58, name: 'Test 1' },
    img: '',
    content: 'This is a test post',
  },
  {
    recipe: { id: 58, name: 'Test 2' },
    img: '',
    content: 'This is test post 2',
  },
  {
    recipe: { id: 58, name: 'Test 3' },
    img: '',
    content: 'This is test post 3',
  },
  {
    recipe: { id: 58, name: 'Test 4' },
    img: '',
    content: 'This is test post 4',
  },
  {
    recipe: { id: 58, name: 'Test 5' },
    img: '',
    content: 'This is test post 5',
  },
  {
    recipe: { id: 58, name: 'Test 6' },
    img: '',
    content: 'This is test post 6',
  },
  {
    recipe: { id: 58, name: 'Test 7' },
    img: '',
    content: 'This is test post 7',
  },
  {
    recipe: { id: 58, name: 'Test 8' },
    img: '',
    content: 'This is test post 8',
  },
  {
    recipe: { id: 58, name: 'Test 9' },
    img: '',
    content: 'This is test post 9',
  },
  {
    recipe: { id: 58, name: 'Test 10' },
    img: '',
    content: 'This is test post 10',
  },
  {
    recipe: { id: 58, name: 'Test 11' },
    img: '',
    content: 'This is test post 11',
  },
  {
    recipe: { id: 58, name: 'Test 12' },
    img: '',
    content: 'This is test post 12',
  },
  {
    recipe: { id: 58, name: 'Test 13' },
    img: '',
    content: 'This is test post 13',
  },
  {
    recipe: { id: 58, name: 'Test 14' },
    img: '',
    content: 'This is test post 14',
  },
  {
    recipe: { id: 58, name: 'Test 15' },
    img: '',
    content: 'This is test post 15',
  },
  {
    recipe: { id: 58, name: 'Test 16' },
    img: '',
    content: 'This is test post 16',
  },
  {
    recipe: { id: 58, name: 'Test 17' },
    img: '',
    content: 'This is test post 17',
  },
  {
    recipe: { id: 58, name: 'Test 18' },
    img: '',
    content: 'This is test post 18',
  },
  {
    recipe: { id: 58, name: 'Test 19' },
    img: '',
    content: 'This is test post 19',
  },
  {
    recipe: { id: 58, name: 'Test 20' },
    img: '',
    content: 'This is test post 20',
  },
  {
    recipe: { id: 58, name: 'Test 21' },
    img: '',
    content: 'This is test post 21',
  },
  {
    recipe: { id: 58, name: 'Test 22' },
    img: '',
    content: 'This is test post 22',
  },
  {
    recipe: { id: 58, name: 'Test 23' },
    img: '',
    content: 'This is test post 23',
  },
]

export const testRecipes: PostRecipe[] = [
  {
    id: 58,
    name: 'test 1',
  },
  {
    id: 58,
    name: 'test 2',
  },
  {
    id: 58,
    name: 'test 3',
  },
  {
    id: 58,
    name: 'test 4',
  },
  {
    id: 58,
    name: 'test 5',
  },
]

export const testRecipesTwo: PostRecipe[] = [
  {
    id: 58,
    name: 'test 6',
  },
  {
    id: 58,
    name: 'test 7',
  },
  {
    id: 58,
    name: 'test 8',
  },
  {
    id: 58,
    name: 'test 9',
  },
  {
    id: 58,
    name: 'test 10',
  },
]
