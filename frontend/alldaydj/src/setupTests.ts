/* eslint-disable import/no-extraneous-dependencies */
import '@testing-library/jest-dom';
import { configure } from 'enzyme';
import Adapter from '@wojtekmaj/enzyme-adapter-react-17';
import 'jest-date-mock';

require('jest-localstorage-mock');

configure({ adapter: new Adapter() });
