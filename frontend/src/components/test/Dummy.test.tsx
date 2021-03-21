import React from 'react';
import { mount } from 'enzyme';
import Dummy from 'components/test/Dummy';

describe('dummy component', () => {
  function mountComponent() {
    return mount(<Dummy />);
  }

  it('snapshot', () => {
    const dummy = mountComponent();
    expect(dummy).toMatchSnapshot();
  });
});
