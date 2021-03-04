import { mount } from 'enzyme';
import React from 'react';
import { ThemeProvider } from 'components/context/ThemeContext';

describe('theme context', () => {
  it('snapshot', () => {
    const component = mount(<ThemeProvider><h1>Hello</h1></ThemeProvider>);
    expect(component).toMatchSnapshot();
  });
});
