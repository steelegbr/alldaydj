import { makeStyles, Theme, createStyles, Box, Grid } from '@material-ui/core'
import React from 'react'

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    toolbar: theme.mixins.toolbar,
    bgImage: {
      backgroundImage: "url('/login_background.jpg')",
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      backgroundSize: 'cover',
      height: '100vh',
      width: '100vw',
      position: 'absolute',
      left: 0,
      top: 0
    },
    loginBox: {
      paddingTop: 10
    }
  })
)

export const AuthenticationWrapper: React.FC = ({ children }) => {
  const classes = useStyles()

  return (
    <Box className={classes.bgImage}>
      <Box className={classes.toolbar}></Box>
      <Grid container justify="center" className={classes.loginBox}>
        <Grid item xs={12} md={4}>
          {children}
        </Grid>
      </Grid>
    </Box>
  )
}
