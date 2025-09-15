import axios from 'axios'

const instance = axios.create({
    baseURL: 'https://turnbenchdemobackend-gphpgyhfe9cngvev.australiacentral-01.azurewebsites.net/api/v1'
})

export default instance