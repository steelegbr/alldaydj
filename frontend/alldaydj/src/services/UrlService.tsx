/* eslint-disable import/prefer-default-export */
export const getUrl = (tenancy: string, path: string): string => `${process.env.REACT_APP_BASE_PROTOCOL}://${tenancy}.${process.env.REACT_APP_BASE_DOMAIN_NAME}${path}`;
