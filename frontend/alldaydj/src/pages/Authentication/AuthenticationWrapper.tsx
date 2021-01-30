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

// eslint-disable-next-line @typescript-eslint/no-empty-interface
interface Props {}

export function AuthenticationWrapper ({ children }: React.PropsWithChildren<Props>): React.ReactElement {
  const classes = useStyles()

  return (
    <Box className={classes.bgImage}>
      <Box className={classes.toolbar}/>
      <Grid className={classes.loginBox} container justify="center">
        <Grid item md={4} xs={12}>
          {children}
        </Grid>
      </Grid>
    </Box>
  )
}
