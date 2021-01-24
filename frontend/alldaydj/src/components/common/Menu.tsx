import { AppBar, Toolbar, IconButton, Typography, Hidden, Drawer, useTheme, Divider, List, ListItemIcon, ListItemText, Grid, makeStyles, createStyles, Theme, ListItem } from '@material-ui/core';
import { Brightness4, Brightness7, LibraryMusic } from '@material-ui/icons';
import MenuIcon from '@material-ui/icons/Menu';
import React from 'react';
import { isAuthenticated } from '../../services/AuthenticationService';
import { AuthenticationContext } from '../context/AuthenticationContext';
import { ThemeContext } from '../context/ThemeContext';

export const Menu = () => {
    const drawerWidth = 240;
    const theme = useTheme();
    const [menuOpen, setMenuOpen] = React.useState(false);
    const themeContext = React.useContext(ThemeContext);
    const authenticationContext = React.useContext(AuthenticationContext);
    const authenticated = isAuthenticated(authenticationContext);

    const useStyles = makeStyles((theme: Theme) => createStyles({
        root: {
            display: 'flex',
        },
        drawer: {
            [theme.breakpoints.up('sm')]: {
                width: drawerWidth,
                flexShrink: 0,
            },
        },
        appBar: {
            marginLeft: drawerWidth,
            zIndex: theme.zIndex.drawer + 1
        },
        menuButton: {
            marginRight: theme.spacing(2),
            [theme.breakpoints.up('sm')]: {
                display: 'none',
            },
        },
        toolbar: theme.mixins.toolbar,
        drawerPaper: {
            width: drawerWidth,
        }
    }));

    const classes = useStyles();
    const container = window.document.body;
    const darkMode = themeContext?.themeSettings.darkMode;

    const handleMenuToggle = () => {
        setMenuOpen(!menuOpen);
    }

    const handleDarkModeToggle = () => {
        if (themeContext) {
            const newThemeSettings = {
                ...themeContext.themeSettings,
                darkMode: !darkMode
            }
            themeContext.setThemeSettings(newThemeSettings);
        }
    }

    const MenuContents = () => {
        return (
            <div>
                <div className={classes.toolbar}/>
                <Divider />
                <List>
                    <ListItem button key="Music Library">
                        <ListItemIcon>
                            <LibraryMusic />
                        </ListItemIcon>
                        <ListItemText primary="Music Library" />
                    </ListItem>
                </List>
            </div>
        )
    }

    return (
        <div className={classes.root}>
            <AppBar position="fixed" className={classes.appBar}>
                <Toolbar>
                    <Grid
                        justify="space-between"
                        alignItems="center"
                        container
                    >
                        <Grid item>
                            {authenticated && (
                                <IconButton
                                    color="inherit"
                                    aria-label="open menu"
                                    edge="start"
                                    onClick={handleMenuToggle}
                                    className={classes.menuButton}
                                >
                                    <MenuIcon />
                                </IconButton>
                            )}
                        </Grid>
                        <Grid item>
                            <Typography variant="h6" noWrap>
                                AllDay DJ
                            </Typography>
                        </Grid>
                        <Grid item>
                            <IconButton
                                color="inherit"
                                arial-label="toggle light / dark mode"
                                edge="end"
                                onClick={handleDarkModeToggle}
                            >
                                {darkMode ? <Brightness4/> : <Brightness7/>}
                            </IconButton>
                        </Grid>
                    </Grid>
                </Toolbar>
            </AppBar>
            {authenticated && (
                <nav aria-label="main menu" className={classes.drawer}>
                    <Hidden smUp implementation="css">
                        <Drawer
                            container={container}
                            variant="persistent"
                            anchor={theme.direction === 'rtl' ? 'right' : 'left'}
                            open={menuOpen}
                            onClose={handleMenuToggle}
                            ModalProps={{
                                keepMounted: true
                            }}
                            classes={{
                                paper: classes.drawerPaper
                            }}
                        >
                            <MenuContents />
                        </Drawer>
                    </Hidden>
                    <Hidden xsDown implementation="css">
                        <Drawer
                            variant="permanent"
                            open
                            classes={{
                                paper: classes.drawerPaper
                            }}
                        >
                            <MenuContents />
                        </Drawer>
                    </Hidden>
                </nav>
            )}
        </div>
    )
}