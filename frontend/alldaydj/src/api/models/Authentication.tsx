export interface ApiLogin {
    email: string,
    password: string
}

export interface ApiLoginResponse {
    refresh: string,
    access: string
}