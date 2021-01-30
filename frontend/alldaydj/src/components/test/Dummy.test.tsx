import React from 'react'
import { shallow } from 'enzyme'
import Dummy from './Dummy'

describe('dummy component', () => {
  function mountComponent () {
    return shallow(<Dummy />)
  }

  it('snapshot', () => {
    const dummy = mountComponent()
    expect(dummy).toMatchSnapshot()
  })
})
