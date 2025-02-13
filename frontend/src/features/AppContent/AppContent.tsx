/*

Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com

*/

/**
 * File name: AppContent.tsx
 * Task - The component defines the routes for the application and decides which component on render on that
 * particular route
 * @author Priyanka Ambawane - dearpriyankasa@gmail.com
 */
import { Routes, Route } from 'react-router-dom'
import HomePage from './HomePage/HomePage'
import About from './HomePage/AboutPage'
import Contact from './HomePage/ContactPage'
import FAQPage from './HomePage/FAQPage'
import RecipeInformation from './RecipeInformation/RecipeInformation'
import RecipeList from './RecipeList/RecipeList'
import Login from './Authentication/Login'
import Profile from './Authentication/Profile'
import Signup from './Authentication/Signup'

import MealPage from './MealPlan/MealPage'

import SmartShoppingList from './ShoppingList/SmartShoppingList'
import RecipeForm from './UserRecipes/RecipeForm'
import { PrivateRoute } from './Authentication/AuthProvider'

export interface SearchBarProps {
  toggleSearchBar: (forceState: boolean | null) => void
}

const AppContent = ({ toggleSearchBar }: SearchBarProps) => {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route
        path="/recipe-list"
        element={<RecipeList toggleSearchBar={toggleSearchBar} />}
      />
      <Route path="/recipe-details/:id" element={<RecipeInformation />} />
      <Route path="/about" element={<About />} />
      <Route path="/contact" element={<Contact />} />
      <Route path="/faq" element={<FAQPage />} />

      {/* Route for Login */}
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />

      {/* Routes if you are logged in*/}
      <Route element={<PrivateRoute />}>
        <Route path="/profile" element={<Profile />} />
      </Route>
      <Route element={<PrivateRoute />}>
        <Route path="/meal" element={<MealPage />} />
      </Route>
      <Route element={<PrivateRoute />}>
        <Route path="/shoppinglist" element={<SmartShoppingList />} />
      </Route>
      <Route element={<PrivateRoute />}>
        <Route path="/create-recipe" element={<RecipeForm />} />
      </Route>
      <Route element={<PrivateRoute />}>
        <Route path="/edit-recipe/:id" element={<RecipeForm />} />
      </Route>
    </Routes>
  )
}

export default AppContent
