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

export interface ApiLogin {
  username: string;
  password: string;
}

export interface ApiLoginResponse {
  refresh: string;
  access: string;
}

export interface ApiRefresh {
  refresh: string;
}

export interface ApiAccess {
  access: string;
}

export interface ApiForgottenPassword {
  email: string;
}

export interface ApiCheckPasswordResetToken {
  token: string;
}

export interface ApiPasswordReset {
  token: string;
  password: string;
}
