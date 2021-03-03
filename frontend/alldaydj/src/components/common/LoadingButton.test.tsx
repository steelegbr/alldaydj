import { mount } from 'enzyme';
import React from 'react';
import LoadingButton from 'components/common/LoadingButton';

describe('loading button', () => {
  const getComponent = (
    loading: boolean,
  ) => mount(<LoadingButton loading={loading}>Test Button</LoadingButton>);

  it('idle state', () => {
    const component = getComponent(false);
    expect(component).toMatchSnapshot();
  });

  it('loading state', () => {
    const component = getComponent(true);
    expect(component).toMatchSnapshot();
  });
});
