import React from "react"
import { BrowserRouter, Switch, Route } from "react-router-dom"
import { Dummy } from "../components/test/Dummy"
import { Login } from "../pages/Authentication/Login"
import { Paths } from "./Paths"
import { PrivateRoute } from "./PrivateRoute"

export const ApplicationRouter = () => (
    <BrowserRouter>
        <Switch>
            <Route path={Paths.auth.login}>
                <Login />
            </Route>
            <PrivateRoute path="/">
                <Dummy />
            </PrivateRoute>
        </Switch>
    </BrowserRouter>
)