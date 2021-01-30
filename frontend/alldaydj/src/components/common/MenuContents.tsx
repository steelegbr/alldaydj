import { createStyles, Divider, List, ListItem, ListItemIcon, ListItemText, makeStyles, Theme } from '@material-ui/core'
import { Domain, ExitToApp, LibraryMusic } from '@material-ui/icons'
import React from 'react'
import { useHistory } from 'react-router-dom'
import { Paths } from '../../routing/Paths'
import { logOut } from '../../services/AuthenticationService'
import { AuthenticationContext } from '../context/AuthenticationContext'

const useStyles = makeStyles((theme: Theme) => createStyles({
  toolbar: theme.mixins.toolbar
}))

export default function MenuContents (): React.ReactElement {
  const history = useHistory()
  const classes = useStyles()
  const authenticationContext = React.useContext(AuthenticationContext)
  const currentTenant = authenticationContext?.authenticationStatus.tenant

  function doLogOut () {
    authenticationContext?.setAuthenticationStatus(logOut())
  }

  function changeTenant (event: React.SyntheticEvent) {
    event.preventDefault()
    history.push(Paths.auth.tenancy)
  }

  function menuItemLibrary () {
    return (
      <ListItem key="Music Library" button>
        <ListItemIcon>
          <LibraryMusic />
        </ListItemIcon>
        <ListItemText primary="Music Library" />
      </ListItem>
    )
  }

  function menuItemTenantChanger () {
    return (
      <ListItem key={Paths.auth.tenancy} button onClick={changeTenant}>
        <ListItemIcon>
          <Domain />
        </ListItemIcon>
        <ListItemText primary="Change Tenant" secondary={`Current: ${currentTenant}`} />
      </ListItem>
    )
  }

  function menuItemLogout () {
    return (
      <ListItem key="Log Out" button onClick={doLogOut}>
        <ListItemIcon>
          <ExitToApp />
        </ListItemIcon>
        <ListItemText primary="Log Out" />
      </ListItem>
    )
  }

  return (
      <div>
        <div className={classes.toolbar} />
        <Divider />
        <List>
          {menuItemLibrary()}
        </List>
        <Divider />
        <List>
          {menuItemTenantChanger()}
          {menuItemLogout()}
        </List>
      </div>
  )
}
