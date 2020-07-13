interface CurrentUserData {
    username: string;
    is_admin: true;
    id: number;
}

export interface CurrentUser {
    user: CurrentUserData,
    id: number;
    user_id: number;
    name: string;
}

export interface LoginReq {
    username: string;
    password: string;
}

export interface LoginRes {
    auth_token: string;
    refresh_token: string;
    data: CurrentUser;
}
