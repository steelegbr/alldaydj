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
