import { createStyles, Divider, List, ListItem, ListItemIcon, ListItemText, makeStyles, Theme } from '@material-ui/core'
import { Domain, ExitToApp, LibraryMusic } from '@material-ui/icons'
import React from 'react'
import { useHistory } from 'react-router-dom'
import { Paths } from '../../routing/Paths'
import { logOut } from '../../services/AuthenticationService'
import { AuthenticationContext } from '../context/AuthenticationContext'

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    toolbar: theme.mixins.toolbar
  })
)

export function MenuContents (): React.ReactElement {
  const history = useHistory()
  const classes = useStyles()
  const authenticationContext = React.useContext(AuthenticationContext)
  const currentTenant = authenticationContext?.authenticationStatus.tenant

  const doLogOut = () => {
    authenticationContext?.setAuthenticationStatus(logOut())
  }

  const changeTenant = (event: React.SyntheticEvent) => {
    event.preventDefault()
    history.push(Paths.auth.tenancy)
  }

  return (
      <div>
        <div className={classes.toolbar} />
        <Divider />
        <List>
          <ListItem button key="Music Library">
            <ListItemIcon>
              <LibraryMusic />
            </ListItemIcon>
            <ListItemText primary="Music Library" />
          </ListItem>
        </List>
        <Divider />
        <List>
          <ListItem button onClick={changeTenant} key={Paths.auth.tenancy}>
            <ListItemIcon>
              <Domain />
            </ListItemIcon>
            <ListItemText primary="Change Tenant" secondary={`Current: ${currentTenant}`} />
          </ListItem>
          <ListItem button key="Log Out" onClick={doLogOut}>
            <ListItemIcon>
              <ExitToApp />
            </ListItemIcon>
            <ListItemText primary="Log Out" />
          </ListItem>
        </List>
      </div>
  )
}
