describe('Login Screen', () => {
    it('Redirect and accessability', () => {
        cy.visit('http://localhost:3000/');
        cy.url().should('eq', 'http://localhost:3000/login/');
        cy.injectAxe();
        cy.checkA11y();
    });
});
