// Credit - https://dev.to/miracool/how-to-manage-user-authentication-with-react-js-3ic5

import { useContext, createContext, ReactNode, useState } from 'react'
import { User, UserCred, UserInfo } from '../api/types'
import { Navigate, Outlet, useNavigate } from 'react-router-dom'
import { useLoginMutation, useSignupMutation } from './userSlice'

type AuthContextType = {
  user: UserInfo | null
  loginAction: (data: UserCred) => void
  signupAction: (data: UserCred) => void
  logOut: () => void
}

interface AuthProviderProps {
  children: ReactNode // Children components to be rendered
}

const AuthContext = createContext<AuthContextType | null>(null)

const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<UserInfo | null>(null)
  const [token, setToken] = useState(localStorage.getItem('site') || '')
  const navigate = useNavigate()
  const [login] = useLoginMutation()
  const [signup] = useSignupMutation()

  // Add to user slice
  const loginAction = async (data: UserCred) => {
    try {
      login(data)
        .unwrap()
        .then((response: UserInfo) => {
          setUser(response)
          navigate('/profile')
          return
        })
        .catch((err) => {
          console.log(err)
        })
    } catch (err) {
      console.error(err)
    }
  }

  const signupAction = async (data: UserCred) => {
    signup(data)
      .unwrap()
      .then((response: UserInfo) => {
        setUser(response)
        navigate('/profile')
        return
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // Add to user slice
  const logOut = () => {
    setUser(null)
    navigate('/login')
  }

  return (
    <AuthContext.Provider value={{ user, loginAction, signupAction, logOut }}>
      {children}
    </AuthContext.Provider>
  )
}

export default AuthProvider

export const useAuth = () => {
  return useContext(AuthContext)
}

export const PrivateRoute = () => {
  const auth = useAuth()
  if (!auth?.user) return <Navigate to="/login" />
  return <Outlet />
}
