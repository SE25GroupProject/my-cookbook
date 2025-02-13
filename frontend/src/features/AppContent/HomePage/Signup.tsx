import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../Authentication/AuthProvider'
import { UserCred } from '../../api/types'
import {
  Alert,
  Box,
  Button,
  Container,
  Link,
  Paper,
  Stack,
  TextField,
  Typography,
} from '@mui/material'
const Signup = () => {
  const auth = useAuth()

  const [email, setEmail] = useState<string>('')
  const [password, setPassword] = useState<string>('')

  const handleSignup = () => {
    const user: UserCred = {
      username: email,
      password: password,
    }
    auth?.signupAction(user)
  }

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 4 }}>
        <Stack spacing={6}>
          <Stack spacing={2}>
            <Typography variant="h3">Signup</Typography>
            {auth?.error && (
              <Alert severity="error" variant="outlined">
                {auth.error}
              </Alert>
            )}
            <TextField
              value={email}
              label="Enter Email"
              onChange={(e) => setEmail(e.target.value)}
            />
            <TextField
              value={[password]}
              label="Enter Password"
              onChange={(e) => setPassword(e.target.value)}
            />
          </Stack>

          <Box>
            <Button onClick={handleSignup}>Signup</Button>
          </Box>
          <Typography variant="body1">
            Already a user? <Link href="/login">Login here</Link>
          </Typography>
        </Stack>
      </Paper>
    </Container>
  )
}

export default Signup
