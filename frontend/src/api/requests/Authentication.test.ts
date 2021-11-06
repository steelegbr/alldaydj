import mockAxios from 'jest-mock-axios';
import { postRefreshToken, userLogin } from './Authentication';

describe('authentication API calls', () => {
  afterEach(() => {
    mockAxios.reset();
  });

  it('user login', () => {
    userLogin({
      username: 'user@example.com',
      password: 'pass',
    });

    expect(mockAxios.post)
      .toHaveBeenCalledWith(
        '/api/token/',
        { username: 'user@example.com', password: 'pass' },
      );
  });

  it('refresh token', () => {
    const refreshData = {
      refresh: 'refresh1',
    };
    postRefreshToken(refreshData);
    expect(mockAxios.post)
      .toHaveBeenCalledWith(
        '/api/token/refresh/',
        refreshData,
      );
  });
});
