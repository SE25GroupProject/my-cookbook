// Credit - https://dev.to/miracool/how-to-manage-user-authentication-with-react-js-3ic5

import { useContext, createContext, ReactNode, useState } from 'react'
import { User, UserCred, UserInfo } from '../api/types'
import { Navigate, Outlet, useLocation, useNavigate } from 'react-router-dom'
import { useLoginMutation, useSignupMutation } from './userSlice'

type AuthContextType = {
  user: UserInfo
  error: string
  loginAction: (data: UserCred) => void
  signupAction: (data: UserCred) => void
  logOut: () => void
  changeRoute: (route: string) => void
  userSignedIn: boolean
}

interface AuthProviderProps {
  children: ReactNode // Children components to be rendered
}

const AuthContext = createContext<AuthContextType | null>(null)

const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<UserInfo>({
    id: parseInt(localStorage.getItem('id') ?? '-1') || -1,
    username: localStorage.getItem('username') || '',
  })
  const [error, setError] = useState('')
  const [route, setRoute] = useState('')
  const navigate = useNavigate()
  const [login] = useLoginMutation()
  const [signup] = useSignupMutation()

  const userSignedIn = user.id >= 0

  const changeRoute = (newRoute: string) => {
    setRoute(newRoute)
  }

  const handleError = (str: string) => {
    setError(str)

    setTimeout(() => {
      setError('')
    }, 5000)
  }

  // Add to user slice
  const loginAction = async (data: UserCred) => {
    login(data)
      .unwrap()
      .then((response: UserInfo) => {
        setUser(response)
        localStorage.setItem('id', response.id.toString())
        localStorage.setItem('username', response.username)
        navigate(route ? route : '/profile')

        setRoute('')
        return
      })
      .catch((err) => {
        console.log(err)
        handleError(err.data.detail)
      })
  }

  const signupAction = async (data: UserCred) => {
    signup(data)
      .unwrap()
      .then((response: UserInfo) => {
        setUser(response)
        localStorage.setItem('id', response.id.toString())
        localStorage.setItem('username', response.username)
        navigate(route ? route : '/profile')
        setRoute('')
        return
      })
      .catch((err) => {
        console.log(err)
        handleError(err.data.detail)
      })
  }

  // Add to user slice
  const logOut = () => {
    localStorage.removeItem('id')
    localStorage.removeItem('username')
    setUser({ id: -1, username: '' })
    navigate('/login')
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        error,
        loginAction,
        signupAction,
        logOut,
        changeRoute,
        userSignedIn,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export default AuthProvider

export const useAuth = () => {
  return useContext(AuthContext)
}

export const PrivateRoute = () => {
  const location = useLocation()
  const auth = useAuth()
  if (!auth?.userSignedIn) {
    auth?.changeRoute(location.pathname)
    return <Navigate to="/login" />
  }
  return <Outlet />
}
