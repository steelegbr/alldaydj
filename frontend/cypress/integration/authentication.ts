/**
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2021 Marc Steele

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

describe('Login Screen', () => {
    beforeEach(() => {
        cy.visit('http://localhost:3000/');
        cy.get('[data-test="toggle-dark-mode"]').click();
    });

    it('Redirect and accessability', () => {
        cy.visit('http://localhost:3000/');
        cy.url().should('eq', 'http://localhost:3000/login/');
        cy.injectAxe();
        cy.checkA11y();
    });

    it('Bad user credentials', () => {
        cy.visit('http://localhost:3000/login/');

        cy.get('[data-test="input-email"]').type('baduser@alldaydj.net');
        cy.get('[data-test="input-password"]').type('Password{enter}');
        cy.get('[data-test="box-error"]').contains('Login failed');

        cy.get('[data-test="button-clear"]').click();
        cy.get('[data-test="box-error"]').should('not.exist');
    });

    it('Good user credentials', () => {
        cy.login();
    });
});

describe('Log out screen', () => {
    it('Redirect to login and accessability', () => {
        cy.visit('http://localhost:3000/logout/');
        cy.get('[data-test="toggle-dark-mode"]').click();
        cy.injectAxe();
        cy.checkA11y();

        cy.get('[data-test="button-login"]').click();

        cy.url().should('eq', 'http://localhost:3000/login/');
    });
})

describe('Forgotten password', () => {
    it('Any e-mail appears successful', () => {
        cy.visit('http://localhost:3000/login/');
        cy.get('[data-test="toggle-dark-mode"]').click();
        cy.get('[data-test="button-reset"]').click();

        cy.url().should('eq', 'http://localhost:3000/request-password-reset/');
        cy.injectAxe();
        cy.checkA11y();

        cy.get('[data-test="input-email"]').type("user@example.com").type('{enter}');

        cy.get('[data-test="box-info"]').contains('If the account exists');
    });
})
