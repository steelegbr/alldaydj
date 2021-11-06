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

// skipcq: JS-0125

import 'cypress-file-upload';

Cypress.Commands.add('login', () => {
    cy.visit('http://localhost:3000/login/');

    cy.get('[data-test="input-email"]').type(Cypress.env('USERNAME'));
    cy.get('[data-test="input-password"]').type(Cypress.env('PASSWORD')).type('{enter}');

    cy.url().should('eq', 'http://localhost:3000/');
})