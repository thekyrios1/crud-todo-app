import axios from 'axios'

const API_BASE = '/todos'

export const api = {
  async getTodos() {
    const response = await axios.get(API_BASE)
    return response.data
  },

  async getTodo(id) {
    const response = await axios.get(`${API_BASE}/${id}`)
    return response.data
  },

  async createTodo(todo) {
    const response = await axios.post(API_BASE, todo)
    return response.data
  },

  async updateTodo(id, todo) {
    const response = await axios.put(`${API_BASE}/${id}`, todo)
    return response.data
  },

  async deleteTodo(id) {
    const response = await axios.delete(`${API_BASE}/${id}`)
    return response.data
  }
}
