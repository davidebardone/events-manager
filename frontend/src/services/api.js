import axios from 'axios';

import TokenService from "./token.service";


// common axios instance with shared configurations
const instance = axios.create({
  headers: {
    "Content-Type": "application/json",
  },
});


// inject access token in requests
instance.interceptors.request.use(
  (config) => {
    const token = TokenService.getLocalAccessToken();
    if (token) {
      config.headers["Authorization"] = 'Bearer ' + token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// handle expired access token
instance.interceptors.response.use(
  (res) => {
    return res;
  },
  async (err) => {
    const originalConfig = err.config;

    if (originalConfig.url !== "/token/" && err.response) {
      // Access token expired (we are not logging in)
      if (err.response.status === 401 && !originalConfig._retry) {
        originalConfig._retry = true;  // avoid infinite loop
        try {
          const rs = await instance.post("/token/refresh/", {
            refresh: TokenService.getLocalRefreshToken(),
          });
          const { access } = rs.data;
          TokenService.updateLocalAccessToken(access);
          return instance(originalConfig);
        } catch (_error) {
          return Promise.reject(_error);
        }
      }
    }
    return Promise.reject(err);
  }
);

export default instance;