export default {
    ENV: process.env.NODE_ENV || 'development',
    API_URI: process.env.VUE_APP_API_URI,
    BASE_URL: process.env.BASE_URL,
    LS_USER_KEY: process.env.VUE_APP_LS_USER_KEY,
    LS_TOKEN_KEY: process.env.VUE_APP_LS_TOKEN_KEY,
    LS_REFRESH_KEY: process.env.VUE_APP_LS_REFRESH_KEY,
}
