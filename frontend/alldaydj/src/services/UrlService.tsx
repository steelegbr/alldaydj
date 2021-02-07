import isDev from './DevelopmentService';

const getUrl = (path: string): string => (isDev() ? `http://localhost:8000${path}` : path);
export default getUrl;
