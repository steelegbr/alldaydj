import { Typography } from '@material-ui/core'
import React from 'react'

export const Dummy = () : React.ReactElement => {
  return (
    <>
      <Typography variant="h1">{'Hello from AllDay DJ'}</Typography>
      <Typography paragraph>{'This is a stand-in component to test routing, etc.'}</Typography>
    </>
  )
}
