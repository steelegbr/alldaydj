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

describe('Cart Operations', () => {
    beforeEach(() => {
        cy.login();
        cy.get('[data-test="toggle-dark-mode"]').click();
    });

    it('Create New Cart', () => {
        cy.get('[data-test="button-library"]').last().click();
        cy.get('[data-test="button-add"]').click();
        cy.url().should('eq', 'http://localhost:3000/cart/');

        cy.get('[data-test="input-label"]').type('TESTCART123');
        cy.get('[data-test="input-display-artist"]').type('Test Artist');
        cy.get('[data-test="input-title"]').type('Test Title');
        cy.get('[data-test="check-sweeper"]').click();

        cy.get('[data-test="input-year"]').clear();
        cy.get('[data-test="input-year"]').type('2021');

        // Disabled due to upload issue in pipleline issues
        // cy.get('[data-test="input-audio-upload"]').attachFile('valid.flac');

        cy.injectAxe();
        cy.checkA11y(null, null, null, true);

        cy.get('[data-test="button-save"]').last().click();
        cy.url().should('eq', 'http://localhost:3000/cart-sync/');
        cy.checkA11y(null, null, null, true);

        cy.get('[data-test="button-forward"]', { timeout: 30000 }).should('be.visible');
        cy.get('[data-test="button-forward"]').click();
        cy.url().should('contain', 'http://localhost:3000/cart/');
    });

    it('Search and Delete', () => {
        cy.get('[data-test="button-library"]').last().click();
        cy.get('[data-test="input-search"]').type('TESTCART123{enter}');
        cy.wait(2000);

        cy.get('[data-test="result-expand"]').first().click();
        cy.injectAxe();
        cy.checkA11y(null, null, null, true);

        cy.get('[data-test="button-delete"]').first().click();
        cy.checkA11y(null, null, null, true);

        cy.get('[data-test="alert-button-delete"]').first().click();
        cy.get('[data-test="result-expand"]', { timeout: 10000 }).should('not.exist');
    });
})