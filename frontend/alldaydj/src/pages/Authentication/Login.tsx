import { Card, Grid, CardContent, FormControl, InputLabel, InputAdornment, Input, Button, CardHeader, CardActions, makeStyles, Theme, createStyles, Box, FormHelperText, CircularProgress } from '@material-ui/core';
import { Email, Lock } from '@material-ui/icons';
import React from 'react';
import { useHistory } from 'react-router-dom';
import { userLogin } from '../../api/requests/Authentication';
import { AuthenticationContext } from '../../components/context/AuthenticationContext';
import { loginUser } from '../../services/AuthenticationService';
import { getLogger } from '../../services/LoggingService';

const useStyles = makeStyles((theme: Theme) => 
    createStyles({
        toolbar: theme.mixins.toolbar,
        bgImage: {
            backgroundImage: `url('/login_background.jpg')`,
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
            backgroundSize: "cover",
            height: "100vh",
            width: "100vw",
            position: "absolute",
            left: 0,
            top: 0
        },
        loginBox: {
            paddingTop: 10
        },
        loginProgress: {
            position: "absolute",
            left: "50%",
            top: "50%",
            marginLeft: -12,
            marginTop: -12
        },
        wrapper: {
            position: "relative"
        },
        errorBox: {
            marginBottom: 10,
            padding: 5
        }
    })
);

type LoginProgress = 
    | "Idle"
    | "Error"
    | "InProgress"
    | "Failed"

interface LoginStatus {
    progress: LoginProgress
    errorEmail?: string,
    errorPassword?: string,
    email: string,
    password: string
}

export const Login = () => {
    let log = getLogger();
    let history = useHistory();
    const classes = useStyles();
    const authenticationContext = React.useContext(AuthenticationContext);
    const [loginStatus, setLoginStatus] = React.useState<LoginStatus>({ 
        progress: "Idle",
        email: "",
        password: ""
    });
    const disableButtons = loginStatus.progress === "InProgress";

    const setEmail = (email: string) => {
        setLoginStatus({
            ...loginStatus,
            errorEmail: undefined,
            email: email
        });
    };

    const setPassword = (password: string) => {
        setLoginStatus({
            ...loginStatus,
            errorPassword: undefined,
            password: password
        });
    };

    const clearForm = () => {
        setLoginStatus({
            progress: "Idle",
            email: '',
            password: '',
            errorEmail: undefined,
            errorPassword: undefined
        });
        log.info("Cleared the login form");
    };

    const attemptLogin = (event: React.SyntheticEvent) => {

        event.preventDefault();

        let newLoginStatus : LoginStatus = {
            progress: "InProgress",
            email: loginStatus.email,
            password: loginStatus.password
        };

        log.info("Starting login validation.")

        let errors = false;

        if (!loginStatus.email) {
            newLoginStatus.errorEmail = "You must supply a username"
            errors = true;
        }

        if (!loginStatus.password) {
            newLoginStatus.errorPassword = "You must supply a password"
            errors = true;
        }

        if (errors) {
            newLoginStatus.progress = "Idle";
            setLoginStatus(newLoginStatus);
            log.error("Login validation failed!");
            return;
        }

        log.info("Login validation complete.")
        setLoginStatus(newLoginStatus);

        userLogin({
            email: newLoginStatus.email,
            password: newLoginStatus.password
        }).then(
            result => {
                log.info('User login success!');
                const user = loginUser(result.data.refresh, result.data.access);
                authenticationContext?.setAuthenticationStatus(user);
                history.push("/");
            },
            error => {
                log.warn(`User login failed - ${error}`);
                setLoginStatus({
                    ...newLoginStatus,
                    progress: "Error"
                });
            })

    }
    
    return (
        <Box className={classes.bgImage}>
            <Box className={classes.toolbar}></Box>
            <Grid
                container 
                justify="center"
                className={classes.loginBox}
            >
                <Grid item xs={12} md={4}>
                    <form onSubmit={attemptLogin}>
                        <Card>
                            <CardHeader title="Login to AllDay DJ" />
                            <CardContent>
                                {loginStatus.progress === "Error" && (
                                    <Box 
                                        bgcolor="error.main" 
                                        boxShadow={3}
                                        className={classes.errorBox}
                                    >
                                        Login failed. Please check your username and password and try again.
                                        If you continue to see this error, please get in touch with support.
                                    </Box>
                                )}
                                    <FormControl fullWidth>
                                        <InputLabel htmlFor="email">Username (e-mail):</InputLabel>
                                        <Input
                                            id="email"
                                            type="email"
                                            error={loginStatus.errorEmail !== undefined}
                                            startAdornment={
                                                <InputAdornment position="start">
                                                    <Email />
                                                </InputAdornment>
                                            }
                                            value={loginStatus.email}
                                            onChange={(event) => { setEmail(event.target.value) }}
                                        />
                                        {loginStatus.errorEmail && (
                                            <FormHelperText error>
                                                {loginStatus.errorEmail}
                                            </FormHelperText>
                                        )}
                                    </FormControl>
                                    <FormControl fullWidth>
                                        <InputLabel htmlFor="password">Password:</InputLabel>
                                        <Input
                                            id="password"
                                            type="password"
                                            error={loginStatus.errorPassword !== undefined}
                                            startAdornment={
                                                <InputAdornment position="start">
                                                    <Lock />
                                                </InputAdornment>
                                            }
                                            value={loginStatus.password}
                                            onChange={(event) => { setPassword(event.target.value) }}
                                        />
                                        {loginStatus.errorPassword && (
                                            <FormHelperText error>
                                                {loginStatus.errorPassword}
                                            </FormHelperText>
                                        )}
                                    </FormControl>
                            </CardContent>
                            <CardActions>
                                <Box className={classes.wrapper}>
                                    <Button 
                                        color="primary" 
                                        variant="contained"
                                        type="submit"
                                        disabled={disableButtons}
                                    >
                                        Login
                                    </Button>
                                    {loginStatus.progress === "InProgress" && (
                                        <CircularProgress size={24} className={classes.loginProgress} />
                                    )}
                                </Box>
                                <Button 
                                    color="secondary" 
                                    variant="outlined"
                                    onClick={clearForm}
                                    disabled={disableButtons}
                                >
                                    Clear
                                </Button>
                            </CardActions>
                        </Card>
                    </form>
                </Grid>
            </Grid>
        </Box>
    )
}