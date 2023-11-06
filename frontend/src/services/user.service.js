import api from './api';
import TokenService from './token.service';

  
const signUp = (userdata) => {
  return api.post("/users/create/", userdata);
}

const login = (username, password) => {
  return api.post("/token/", {'username': username, 'password': password})
  .then(res => {
    if (res.data.access){
      TokenService.setUser(res.data);
    }
    return res.data;
  })
}


const UserService = {
  signUp,
  login
}

export default UserService;
