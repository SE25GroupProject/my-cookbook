import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../Authentication/AuthProvider'
import { UserCred } from '../../api/types'
import { Alert } from '@mui/material'

export interface LoginParam {
  intendedRoute: string
}

const Login = () => {
  const auth = useAuth()

  const [email, setEmail] = useState<string>('')
  const [password, setPassword] = useState<string>('')

  const handleLogin = () => {
    const user: UserCred = {
      username: email,
      password: password,
    }
    auth?.loginAction(user)
  }

  return (
    <div>
      <h2>Login</h2>
      {auth?.error && (
        <Alert severity="error" variant="outlined">
          {auth.error}
        </Alert>
      )}
      <div>
        <input
          type="email"
          placeholder="Enter email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <div>
        <input
          type="password"
          placeholder="Enter password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>

      <button onClick={handleLogin}>Login</button>
      <p>
        Don't have an account? <a href="/signup">Signup here</a>
      </p>
    </div>
  )
}

export default Login
