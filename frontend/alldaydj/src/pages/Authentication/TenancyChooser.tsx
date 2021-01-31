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
  Select,
} from '@material-ui/core';
import React, { useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { ApiTenancy } from '../../api/models/Authentication';
import { getTenancies } from '../../api/requests/Authentication';
import { AuthenticationContext } from '../../components/context/AuthenticationContext';
import { setTenant } from '../../services/AuthenticationService';
import { getLogger } from '../../services/LoggingService';
import AuthenticationWrapper from './AuthenticationWrapper';

const useStyles = makeStyles(() => createStyles({
  errorBox: {
    marginBottom: 10,
    padding: 5,
  },
}));

export default function TenancyChooser(): React.ReactElement {
  const log = getLogger();
  const history = useHistory();
  const classes = useStyles();
  const authenticationContext = React.useContext(AuthenticationContext);
  const token = authenticationContext?.authenticationStatus.accessToken;
  const [tenancies, setTenancies] = React.useState<ApiTenancy[]>([]);
  const [error, setError] = React.useState<string>('');
  const [selectedTenant, setSelectedTenant] = React.useState<string>('');

  useEffect(() => {
    if (token) {
      log.info('Updating list of tenancies.');
      getTenancies(token).then(
        (response) => {
          setError('');
          setTenancies(response.data);
        },
        (tokenUpdateError) => {
          log.error(tokenUpdateError);
          setError('Failed to load the list of tenancies for the current user.');
        },
      );
    }
  }, [token, log]);

  function doSetTenant(tenant: string) {
    if (authenticationContext) {
      const { authenticationStatus, setAuthenticationStatus } = authenticationContext;
      const newAuthenticationStatus = setTenant(tenant, authenticationStatus);
      setAuthenticationStatus(newAuthenticationStatus);
      log.info(`Set tenant to ${tenant}.`);
      history.push('/');
    }
    log.error(`Cannot set tenant to ${tenant} as we don't have an authentication context.`);
  }

  function changeSelectedTenant(event: React.ChangeEvent<{ value: unknown }>) {
    setSelectedTenant(event.target.value as string);
  }

  if (tenancies && tenancies.length === 1) {
    doSetTenant(tenancies[0].slug);
  }

  const buttonDisabled = !selectedTenant;
  if (buttonDisabled && tenancies.length > 0) {
    setSelectedTenant(tenancies[0].slug);
  }

  function handleSelectTenant(event: React.SyntheticEvent) {
    if (selectedTenant) {
      event.preventDefault();
      doSetTenant(selectedTenant);
    }
  }

  function errorCard() {
    return (
      <Card>
        <CardHeader title="Choose a Tenancy" />
        <CardContent>
          <Box bgcolor="error.main" boxShadow={3} className={classes.errorBox}>
            Failed to load the list of tenancies to select from.
          </Box>
        </CardContent>
      </Card>
    );
  }

  function chooserCard() {
    return (
      <Card>
        <CardHeader title="Choose a Tenancy" />
        <CardContent>
          <Select onChange={changeSelectedTenant} value={selectedTenant}>
            {tenancies.map((currentTenant) => (
              <MenuItem key={currentTenant.slug} value={currentTenant.slug}>
                {currentTenant.name}
              </MenuItem>
            ))}
          </Select>
        </CardContent>
        <CardActions>
          <Button color="primary" disabled={buttonDisabled} type="submit" variant="contained">
            Choose
          </Button>
        </CardActions>
      </Card>
    );
  }

  if (error) {
    return (
      <AuthenticationWrapper>
        {errorCard()}
      </AuthenticationWrapper>
    );
  }

  return (
    <AuthenticationWrapper>
      <form onSubmit={handleSelectTenant}>
        {chooserCard()}
      </form>
    </AuthenticationWrapper>
  );
}
