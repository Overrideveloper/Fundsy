import { BehaviorSubject } from 'rxjs';
import { CurrentUser, LoginReq, LoginRes } from '@/types/auth';
import { getFromLS, saveToLS, removeFromLS } from './storage';
import config from '@/common/config';
import http from './http';
import { Response } from '@/types/http';

const saveRefreshToken = (token: string) => saveToLS(<string> config.LS_REFRESH_KEY, token); 

function saveCurrentUser(data: CurrentUser) {
    saveToLS(<string> config.LS_USER_KEY, data);
    currentUser.next(data);
}

export const currentUser = new BehaviorSubject<CurrentUser | null>(getFromLS(<string> config.LS_USER_KEY));

export function getAuthToken() {
    return getFromLS<string>(<string> config.LS_TOKEN_KEY);
}

export function getRefreshToken() {
    return getFromLS<string>(<string> config.LS_REFRESH_KEY);
}

export function saveAuthToken(token: string) {
    saveToLS(<string> config.LS_TOKEN_KEY, token);
}

function removeStoredDataOnLogout() {
    removeFromLS(<string> config.LS_USER_KEY);
    removeFromLS(<string> config.LS_REFRESH_KEY);
    removeFromLS(<string> config.LS_TOKEN_KEY);
    currentUser.next(null);
}

export function login(credentials: LoginReq) {
    return http.post<Response<LoginRes>>('/auth/login', credentials)
        .then(({ data }) => {
            saveAuthToken(data.data.auth_token);
            saveRefreshToken(data.data.refresh_token);
            saveCurrentUser(data.data.data);
            return Promise.resolve(true);
        }).catch(err => Promise.reject(err));
}

export function logout() {
    return http.post<Response<boolean>>('/auth/invalidate_token', { refresh_token: getRefreshToken() })
        .then(_ => {
            removeStoredDataOnLogout();
            return Promise.resolve(true);
        }).catch(err => Promise.reject(err));
}
