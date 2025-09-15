import axios from './request.ts'

export const getGames = (params: any) => axios.get('/games', { params })

export const getGameDetail = (game_id: any) => axios.get(`/game/${game_id}`)

export const getSetUps = (params: any) => axios.get('/turnbench/setups', { params })

export const getSetUpDetail = (setup_id: any) => axios.get(`/turnbench/setups/${setup_id}`)

export const getProviders = (params: any) => axios.get(`/providers`, { params })

export const createProvider = (params: any) => axios.post(`/providers`, params)

export const updateProvider = (provider_id: any, params: any) =>
  axios.put(`/providers/${provider_id}`, params)

export const deleteProviders = (provider_id: any) => axios.delete(`/providers/${provider_id}`)

export const getllms = (params: any) => axios.get(`/llms`, {params})

export const getllmDetail = (llm_id: any) => axios.get(`/llms/${llm_id}`)

export const createModel = (params: any) => axios.post(`/llms`, params)

export const updateModel = (llm_id: any, params: any) => axios.put(`/llms/${llm_id}`, params)

export const deleteModel = (llm_id: any) => axios.delete(`/llms/${llm_id}`)

export const getSessions = (params: any) => axios.get('/turnbench/sessions', { params })

export const getSessionDetail = (session_id: string) => axios.get(`/turnbench/sessions/${session_id}`)

export const createSession = (params: any) => axios.post(`/turnbench/sessions`, params)

export const copySession = (session_id: any, new_model_id: any, new_turn_data: any) =>
  axios.post(`/turnbench/sessions/${session_id}/copy`, {
    new_model_id: new_model_id,
    new_turn_data: new_turn_data,
  })

export const playTurn = (session_id: any, params: any) =>
  axios.post(`/turnbench/sessions/${session_id}/play/turn`, params)

export const saveSession = (session_id: any, save_to_db: any) =>
  axios.post(`/turnbench/sessions/${session_id}/save`, { save_to_db })

export const getSessionHistory = () => axios.get(`/turnbench/sessions`)

export const getSessionDetailTurnhistory = (session_id: any) =>
  axios.get(`/turnbench/sessions/${session_id}/history/turn`)

export const reloadSession = (session_id: any) => axios.post(`/turnbench/sessions/${session_id}/reload`)

export const updateSession = (session_id: string, params: any) =>
  axios.put(`/turnbench/sessions/${session_id}`, { new_turn_data: params })

export const getDependencies = (params: any) => axios.post(`/dependencies`, params)
