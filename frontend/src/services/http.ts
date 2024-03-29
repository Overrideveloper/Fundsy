import axios, { AxiosInstance, AxiosResponse, AxiosError, AxiosRequestConfig } from 'axios'
import config from '@/common/config'
import { currentUser, getRefreshToken, saveAuthToken, getAuthToken } from './auth';
import { Response } from '@/types/http';

const DEFAULT_ERROR = 'An error occurred. Please check your internet connection and try again.';

const instance: AxiosInstance = axios.create({ baseURL: config.API_URI });

function setAuthorizationHeader(config: AxiosRequestConfig) {
    const authToken = getAuthToken();

    if (authToken) {
        config.headers['Authorization'] = `Bearer ${authToken}`;
    }
}

function refreshToken(): Promise<boolean> {
    const user_id = currentUser.getValue()?.user_id;
    const refresh_token = getRefreshToken();

    return instance.post<Response<string>>('/auth/refresh_token', { refresh_token, user_id })
        .then(({ data }) => {
            saveAuthToken(data.data);
            return Promise.resolve(true);
        });
}

function handleSuccess(response: AxiosResponse): AxiosResponse {
    return response;
}

function handleError(error: AxiosError<Response<any>>): Promise<AxiosResponse> {
    const status = error.response ? error.response.status : null;
    const message = error.response?.data.message;


    if (status === 401 || (status === 403 && message === 'Not authenticated')) {
        return refreshToken().then(_ => {
            setAuthorizationHeader(error.config);
            error.config.baseURL = undefined;
            return instance.request(error.config);
        });
    }

    return Promise.reject(message || DEFAULT_ERROR);
}

instance.interceptors.request.use(config => {
    setAuthorizationHeader(config);
    return config;
});

instance.interceptors.response.use(response => handleSuccess(response), error => handleError(error));

export default instance;
