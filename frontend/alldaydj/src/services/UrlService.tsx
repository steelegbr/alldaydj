export const getUrl = (tenancy: string, path: string) => {
    return `${process.env.REACT_APP_BASE_PROTOCOL}://${tenancy}.${process.env.REACT_APP_BASE_DOMAIN_NAME}${path}`;
}