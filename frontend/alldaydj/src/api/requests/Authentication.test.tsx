import mockAxios from 'jest-mock-axios'
import { HttpResponse } from 'jest-mock-axios/dist/lib/mock-axios-types'
import { ApiLoginResponse } from '../models/Authentication'
import { getTenancies, postRefreshToken, userLogin } from './Authentication'

describe('authentication API calls', () => {
  beforeEach(() => {
    mockAxios.reset()
  })

  it('user login', async () => {
    await userLogin({
      email: 'user@example.com',
      password: 'pass'
    })

    expect(mockAxios.post)
      .toHaveBeenCalledWith(
        'undefined://login.undefined/api/token/',
        { email: 'user@example.com', password: 'pass' }
      )
  })

  it('get tenancy list', async () => {
    await getTenancies('token1')
    expect(mockAxios.get)
      .toHaveBeenCalledWith(
        'undefined://login.undefined/api/token/tenancies/',
        {
          headers: {
            Authorization: 'Bearer token1'
          }
        }
      )
  })

  it('refresh token', async () => {
    const refreshData = {
      refresh: 'refresh1'
    }
    await postRefreshToken(refreshData)
    expect(mockAxios.post)
      .toHaveBeenCalledWith(
        'undefined://login.undefined/api/token/refresh/',
        refreshData
      )
  })
})
