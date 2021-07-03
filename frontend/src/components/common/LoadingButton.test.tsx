/**
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2021 Marc Steele

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

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
