import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  createStyles,
  makeStyles,
  MenuItem,
  Select
} from '@material-ui/core'
import React, { useEffect } from 'react'
import { useHistory } from 'react-router-dom'
import { ApiTenancy } from '../../api/models/Authentication'
import { getTenancies } from '../../api/requests/Authentication'
import { AuthenticationContext } from '../../components/context/AuthenticationContext'
import { setTenant } from '../../services/AuthenticationService'
import { getLogger } from '../../services/LoggingService'
import { AuthenticationWrapper } from './AuthenticationWrapper'

const useStyles = makeStyles(() =>
  createStyles({
    errorBox: {
      marginBottom: 10,
      padding: 5
    }
  })
)

export const TenancyChooser = (): React.ReactElement => {
  const log = getLogger()
  const history = useHistory()
  const classes = useStyles()
  const authenticationContext = React.useContext(AuthenticationContext)
  const token = authenticationContext?.authenticationStatus.accessToken
  const [tenancies, setTenancies] = React.useState<ApiTenancy[]>([])
  const [error, setError] = React.useState<string>('')
  const [selectedTenant, setSelectedTenant] = React.useState<string>('')

  useEffect(() => {
    if (token) {
      log.info('Updating list of tenancies.')
      getTenancies(token).then(
        (response) => {
          setError('')
          setTenancies(response.data)
        },
        (error) => {
          log.error(error)
          setError('Failed to load the list of tenancies for the current user.')
        }
      )
    }
  }, [token, log])

  const doSetTenant = (tenant: string) => {
    if (authenticationContext) {
      const { authenticationStatus, setAuthenticationStatus } = authenticationContext
      const newAuthenticationStatus = setTenant(tenant, authenticationStatus)
      setAuthenticationStatus(newAuthenticationStatus)
      log.info(`Set tenant to ${tenant}.`)
      history.push('/')
    }
    log.error(`Cannot set tenant to ${tenant} as we don't have an authentication context.`)
  }

  const changeSelectedTenant = (event: React.ChangeEvent<{ value: unknown }>) => {
    setSelectedTenant(event.target.value as string)
  }

  // if (tenancies && tenancies.length === 1) {
  //    doSetTenant(tenancies[0].slug);
  // }

  const buttonDisabled = !selectedTenant
  if (buttonDisabled && tenancies.length > 0) {
    setSelectedTenant(tenancies[0].slug)
  }

  const handleSelectTenant = (event: React.SyntheticEvent) => {
    if (selectedTenant) {
      event.preventDefault()
      doSetTenant(selectedTenant)
    }
  }

  if (error) {
    return (
      <AuthenticationWrapper>
        <Card>
          <CardHeader title="Choose a Tenancy" />
          <CardContent>
            <Box bgcolor="error.main" boxShadow={3} className={classes.errorBox}>
              {'Failed to load the list of tenancies to select from.'}
            </Box>
          </CardContent>
        </Card>
      </AuthenticationWrapper>
    )
  }

  return (
    <AuthenticationWrapper>
      <form onSubmit={handleSelectTenant}>
        <Card>
          <CardHeader title="Choose a Tenancy" />
          <CardContent>
            <Select value={selectedTenant} onChange={changeSelectedTenant}>
              {tenancies.map((currentTenant) => (
                <MenuItem value={currentTenant.slug} key={currentTenant.slug}>{currentTenant.name}</MenuItem>
              ))}
            </Select>
          </CardContent>
          <CardActions>
            <Button color="primary" variant="contained" type="submit" disabled={buttonDisabled}>
              {'Choose'}
            </Button>
          </CardActions>
        </Card>
      </form>
    </AuthenticationWrapper>
  )
}
