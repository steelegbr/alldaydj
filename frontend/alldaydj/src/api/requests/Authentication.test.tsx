import mockAxios from 'jest-mock-axios';
import { postRefreshToken, userLogin } from './Authentication';

describe('authentication API calls', () => {
  beforeEach(() => {
    mockAxios.reset();
  });

  it('user login', async () => {
    await userLogin({
      username: 'user@example.com',
      password: 'pass',
    });

    expect(mockAxios.post)
      .toHaveBeenCalledWith(
        '/api/token/',
        { username: 'user@example.com', password: 'pass' },
      );
  });

  it('refresh token', async () => {
    const refreshData = {
      refresh: 'refresh1',
    };
    await postRefreshToken(refreshData);
    expect(mockAxios.post)
      .toHaveBeenCalledWith(
        '/api/token/refresh/',
        refreshData,
      );
  });
});
