import { mount } from 'enzyme';
import React from 'react';
import { ThemeProvider } from './ThemeContext';

describe('theme context', () => {
  it('snapshot', () => {
    const component = mount(<ThemeProvider><h1>Hello</h1></ThemeProvider>);
    expect(component).toMatchSnapshot();
  });
});
