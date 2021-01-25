export interface ApiLogin {
    email: string,
    password: string
}

export interface ApiLoginResponse {
    refresh: string,
    access: string
}

export interface ApiTenancy {
    name: string,
    slug: string
}