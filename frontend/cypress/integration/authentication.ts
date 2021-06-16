describe('Login Screen', () => {
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
        cy.visit('http://localhost:3000/login/');

        cy.get('[data-test="input-email"]').type(Cypress.env('USERNAME'));
        cy.get('[data-test="input-password"]').type(Cypress.env('PASSWORD')).type('{enter}');

        cy.url().should('eq', 'http://localhost:3000/');
    });
});

describe('Log out screen', () => {
    it('Redirect to login and accessability', () => {
        cy.visit('http://localhost:3000/logout/');
        cy.injectAxe();
        cy.checkA11y();

        cy.get('[data-test="button-login"]').click();

        cy.url().should('eq', 'http://localhost:3000/login/');
    });
})

describe('Forgotten password', () => {
    it('Any e-mail appears successful', () => {
        cy.visit('http://localhost:3000/login/');
        cy.get('[data-test="button-reset"]').click();

        cy.url().should('eq', 'http://localhost:3000/request-password-reset/');
        cy.injectAxe();
        cy.checkA11y();

        cy.get('[data-test="input-email"]').type("user@example.com").type('{enter}');

        cy.get('[data-test="box-info"]').contains('If the account exists');
    });
})
