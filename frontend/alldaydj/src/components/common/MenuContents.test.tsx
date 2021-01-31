import React from 'react'
import { mount } from 'enzyme'
import MenuContents from './MenuContents'

describe('menu contents', () => {
  const mockPush = jest.fn()

  beforeAll(() => {
    jest.mock('react-router-dom', () => ({
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      ...jest.requireActual('react-router-dom') as any,
      useHistory: () => ({
        push: mockPush
      })
    }))
  })

  beforeEach(() => {
    jest.resetAllMocks()
  })

  function mountComponent () {
    return mount(<MenuContents />)
  }

  it('snapshot', () => {
    const component = mountComponent()
    expect(component).toMatchSnapshot()
  })

  it('change tenant should redirect', () => {
    const component = mountComponent()
    const tenantSelectorButton = component.find({ primary: 'Choose Tenant' })
    console.log(tenantSelectorButton.debug())
    expect(tenantSelectorButton).toBe({})
  })
})
