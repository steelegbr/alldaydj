import { generateHeaders } from './Helpers'

it('generate headers correctly', () => {
  const expected = {
    headers: {
      Authorization: 'Bearer: token123'
    }
  }
  const actual = generateHeaders('token123')
  expect(actual).toStrictEqual(expected)
})
