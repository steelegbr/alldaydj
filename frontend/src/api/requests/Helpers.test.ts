import { generateRequestConfig } from 'api/requests/Helpers';
import { getTokenFromLocalStorage } from 'services/AuthenticationService';

const mockToken = getTokenFromLocalStorage as jest.Mock;
jest.mock('services/AuthenticationService');

it('generate headers correctly', () => {
  mockToken.mockReturnValue('TOKEN123');
  const expected = {
    headers: {
      Authorization: 'Bearer TOKEN123',
    },
  };
  const actual = generateRequestConfig();
  expect(actual).toStrictEqual(expected);
});
