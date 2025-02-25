import React, { useState, useEffect } from 'react'
import axios from 'axios'
import {
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  Checkbox,
  IconButton,
  Typography,
  InputAdornment,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete'
import { jsPDF } from 'jspdf'
import shoppingListImage from './image/shopping-list.jpg'
import { useTheme } from '../../Themes/themeContext'
import { ShoppingItem, ShoppingItemRequest } from '../../api/types'
import {
  useGetShoppingListQuery,
  useRemoveFromShoppingListMutation,
  useUpdateShoppingListMutation,
} from './ShoppingListSlice'
import { useAuth } from '../Authentication/AuthProvider'

const SmartShoppingList: React.FC = () => {
  const { theme } = useTheme()
  const auth = useAuth()

  // const [listItems, setListItems] = useState<ShoppingItem[]>([])
  const [newItem, setNewItem] = useState<string>('')
  const [quantity, setQuantity] = useState<number>(1)
  const [unit, setUnit] = useState<string>('')
  const [isProcessing, setIsProcessing] = useState<boolean>(false)
  // const [loading, setLoading] = useState<boolean>(false)

  const userId = auth?.user.id ?? -1
  const { data: listItems, isLoading } = useGetShoppingListQuery(userId, {
    skip: userId == -1,
  })

  const [updateShoppingList] = useUpdateShoppingListMutation()
  const [removeFromShoppingList] = useRemoveFromShoppingListMutation()

  const units = [
    'kg',
    'g',
    'lb',
    'oz',
    'liter',
    'ml',
    'dozen',
    'bunch',
    'head',
    'loaf',
    'piece',
    'cup',
    'tablespoon',
    'teaspoon',
    'can',
    'pack',
    'box',
    'jar',
    'bottle',
    'slice',
    'packet',
  ]

  const addItemToList = async () => {
    if (!newItem.trim() || !unit.trim()) {
      window.alert('Please fill in all fields.')
      return
    }
    setIsProcessing(true)
    if (auth) {
      try {
        const newItemData: ShoppingItemRequest = {
          userId: auth?.user.id,
          name: newItem,
          quantity,
          unit,
          checked: false,
        }

        updateShoppingList(newItemData)

        setNewItem('')
        setQuantity(1)
        setUnit('')
      } catch (error) {
        console.error('Error adding item:', error)
      } finally {
        setIsProcessing(false)
      }
    }
  }

  const toggleItemCheck = async (item: ShoppingItem) => {
    if (!listItems || !auth) return

    let req: ShoppingItemRequest = {
      name: item.name,
      quantity: item.quantity,
      unit: item.unit,
      checked: !item.checked,
      userId: auth?.user.id,
    }

    updateShoppingList(req)
  }

  const deleteItem = async (itemName: string) => {
    if (!auth) return

    let req: ShoppingItemRequest = {
      name: itemName,
      quantity: 0,
      unit: '',
      checked: false,
      userId: auth?.user.id,
    }

    removeFromShoppingList(req)
  }

  const exportListToPDF = () => {
    if (!listItems) return

    const doc = new jsPDF()

    doc.setFontSize(18)
    doc.text('Shopping List', 20, 20)

    let yOffset = 30
    listItems.forEach((item) => {
      doc.setFontSize(12)
      doc.text(
        `${item.name} - Quantity: ${item.quantity} ${item.unit}`,
        20,
        yOffset
      )
      yOffset += 10
    })

    doc.save('shopping_list.pdf')
  }

  return (
    <div
      style={{ width: '40%', textAlign: 'center', fontFamily: 'RobotoThin' }}
    >
      <h2>Smart Shopping List</h2>
      <img
        src={shoppingListImage}
        alt="Shopping List"
        style={{
          width: 'auto',
          height: 'auto',
          maxWidth: '100%',
          maxHeight: '100%',
          objectFit: 'cover',
          padding: 0,
          margin: 0,
        }}
      />
      <TextField
        label="Add a shopping item"
        value={newItem}
        onChange={(e) => setNewItem(e.target.value)}
        fullWidth
        variant="outlined"
        disabled={isProcessing}
        margin="normal"
        sx={{
          '& .MuiOutlinedInput-root': {
            '& fieldset': {
              borderColor: theme.color,
            },
            '&:hover fieldset': {
              borderColor: theme.headerColor,
            },
            '&.Mui-focused fieldset': {
              borderColor: theme.color,
            },
            '& .MuiInputBase-input': {
              color: theme.color,
            },
          },
          '& .MuiInputLabel-root': {
            color: theme.color,
          },
          '& .MuiInputLabel-root.Mui-focused': {
            color: theme.color,
          },
        }}
      />
      <TextField
        label="Quantity"
        type="number"
        value={quantity}
        onChange={(e) => setQuantity(Number(e.target.value))}
        fullWidth
        variant="outlined"
        margin="normal"
        sx={{
          '& .MuiOutlinedInput-root': {
            '& fieldset': {
              borderColor: theme.color,
            },
            '&:hover fieldset': {
              borderColor: theme.color,
            },
            '&.Mui-focused fieldset': {
              borderColor: theme.color,
            },
            '& .MuiInputBase-input': {
              color: theme.color,
            },
          },
          '& .MuiInputLabel-root': {
            color: theme.color,
          },
          '& .MuiInputLabel-root.Mui-focused': {
            color: theme.color,
          },
        }}
      />
      <FormControl
        fullWidth
        variant="outlined"
        margin="normal"
        sx={{
          '& .MuiOutlinedInput-root': {
            '& fieldset': {
              borderColor: theme.color,
            },
            '&:hover fieldset': {
              borderColor: theme.color,
            },
            '&.Mui-focused fieldset': {
              borderColor: theme.color,
            },
          },
          '& .MuiSelect-select': {
            textAlign: 'left',
          },
          '& .MuiInputLabel-root': {
            color: theme.color,
          },
          '& .MuiInputLabel-root.Mui-focused': {
            color: theme.color,
          },
        }}
      >
        <InputLabel>Unit</InputLabel>
        <Select
          value={unit}
          onChange={(e) => setUnit(e.target.value)}
          label="Unit"
          disabled={isProcessing}
          MenuProps={{
            PaperProps: {
              style: {
                maxHeight: 200,
                overflowY: 'auto',
              },
            },
          }}
        >
          {units.map((unitOption, index) => (
            <MenuItem key={index} value={unitOption}>
              {unitOption}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <Button
        variant="contained"
        color="primary"
        onClick={addItemToList}
        disabled={isProcessing}
        fullWidth
        sx={{
          backgroundColor: theme.headerColor,
          '&:hover': {
            backgroundColor: theme.color,
          },
          marginBottom: '20px',
        }}
      >
        {isProcessing ? 'Adding...' : 'Add Item'}
      </Button>
      {isLoading ? (
        <CircularProgress />
      ) : !listItems ? (
        <Typography>Oops! No Items.</Typography>
      ) : (
        <List>
          {listItems.map((item) => (
            <ListItem key={item.name} style={{ marginBottom: '10px' }}>
              <Checkbox
                checked={item.checked}
                onChange={() => toggleItemCheck(item)}
                sx={{
                  '& .MuiSvgIcon-root': {
                    color: 'black',
                  },
                  '&.Mui-checked .MuiSvgIcon-root': {
                    color: 'green',
                  },
                  '&:hover': {
                    backgroundColor: 'transparent',
                  },
                }}
              />
              <ListItemText
                primary={`${item.name} (Unit: ${item.unit})`}
                secondary={`Quantity: ${item.quantity}`}
              />
              <IconButton onClick={() => deleteItem(item.name)} color="error">
                <DeleteIcon />
              </IconButton>
            </ListItem>
          ))}
        </List>
      )}

      <div>
        <Button
          variant="outlined"
          onClick={exportListToPDF}
          style={{ marginTop: '20px' }}
          fullWidth
          sx={{
            borderColor: theme.headerColor,
            color: theme.color,
            '&:hover': {
              borderColor: theme.color,
              color: theme.headerColor,
            },
          }}
        >
          Export List
        </Button>
      </div>
    </div>
  )
}

export default SmartShoppingList
