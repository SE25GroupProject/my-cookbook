import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'
import { testPosts } from '../AppContent/testVariables'

export const handlers = [
  http.get('http://localhost:8000/posts/', () => {
    return HttpResponse.json(testPosts)
  }),
  http.get('http://localhost:8000/meal-plan/1', () => {
    return HttpResponse.json([
      {
        day: 0,
        recipe: { name: 'Pasta', instructions: ['Boil water', 'Cook pasta'] },
      },
      {
        day: 2,
        recipe: {
          name: 'Salad',
          instructions: ['Chop vegetables', 'Mix dressing'],
        },
      },
    ])
  }),
]

export const server = setupServer(...handlers)
