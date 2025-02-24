/*

Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com

*/

import React from 'react'
import first from '../images/first.jpg'
import second from '../images/second.jpg'
import third from '../images/third.jpg'
import fourth from '../images/fourth.jpg'
import fifth from '../images/fifth.jpg'
import sixth from '../images/sixth.jpg'
import seventh from '../images/seventh.jpg'
import eighth from '../images/eighth.jpg'
import nineth from '../images/nineth.jpg'
import tenth from '../images/tenth.jpg'
import { useTheme } from '../../Themes/themeContext'

const HomePage = () => {
  const { theme } = useTheme()
  return (
    <div style={{ backgroundColor: theme.background, color: theme.color }}>
      <table>
        <tbody>
          <tr>
            <td>
              <img src={first} alt="first image" />
            </td>
            <td>
              <img src={second} alt="second image" />
            </td>
            <td>
              <img src={third} alt="third image" />
            </td>
            <td>
              <img src={fourth} alt="fourth image" />
            </td>
            <td>
              <img src={fifth} alt="fifth image" />
            </td>
          </tr>
          <tr>
            <td>
              <img src={sixth} alt="sixth image" />
            </td>
            <td>
              <img src={seventh} alt="seventh image" />
            </td>
            <td>
              <img src={eighth} alt="eighth image" />
            </td>
            <td>
              <img src={nineth} alt="nineth image" />
            </td>
            <td>
              <img src={tenth} alt="tenth image" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}

export default HomePage
