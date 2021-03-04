import { generateRequestConfig } from 'api/requests/Helpers';

it('generate headers correctly', () => {
  const expected = {
    headers: {
      Authorization: 'Bearer token123',
    },
  };
  const actual = generateRequestConfig('token123');
  expect(actual).toStrictEqual(expected);
});
