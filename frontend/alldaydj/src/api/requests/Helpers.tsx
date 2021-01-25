export const generateHeaders = (token: string) => {
    return {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    };
}