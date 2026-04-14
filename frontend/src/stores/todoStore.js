import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '../api.js'

export const useTodoStore = defineStore('todo', () => {
  const todos = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchTodos = async () => {
    loading.value = true
    error.value = null
    try {
      todos.value = await api.getTodos()
    } catch (err) {
      error.value = err.message || 'Failed to fetch todos'
    } finally {
      loading.value = false
    }
  }

  const createTodo = async (todoData) => {
    console.log('createTodo called with:', todoData)
    loading.value = true
    error.value = null
    try {
      const newTodo = await api.createTodo(todoData)
      console.log('API response:', newTodo)
      todos.value.push(newTodo)
      return newTodo
    } catch (err) {
      console.error('createTodo API error:', err)
      error.value = err.message || 'Failed to create todo'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateTodo = async (id, todoData) => {
    loading.value = true
    error.value = null
    try {
      const updatedTodo = await api.updateTodo(id, todoData)
      const index = todos.value.findIndex(t => t.id === id)
      if (index !== -1) {
        todos.value[index] = updatedTodo
      }
      return updatedTodo
    } catch (err) {
      error.value = err.message || 'Failed to update todo'
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteTodo = async (id) => {
    loading.value = true
    error.value = null
    try {
      await api.deleteTodo(id)
      todos.value = todos.value.filter(t => t.id !== id)
    } catch (err) {
      error.value = err.message || 'Failed to delete todo'
      throw err
    } finally {
      loading.value = false
    }
  }

  const toggleComplete = async (id) => {
    const todo = todos.value.find(t => t.id === id)
    if (!todo) return
    
    try {
      await updateTodo(id, { ...todo, completed: !todo.completed })
    } catch (err) {
      error.value = err.message || 'Failed to toggle completion'
    }
  }

  return {
    todos,
    loading,
    error,
    fetchTodos,
    createTodo,
    updateTodo,
    deleteTodo,
    toggleComplete
  }
})
