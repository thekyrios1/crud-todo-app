<script setup>
import { ref, computed, onMounted } from 'vue'
import TodoForm from '../components/TodoForm.vue'
import { useTodoStore } from '../stores/todoStore.js'
import { useDark, useToggle } from '@vueuse/core'

const isDark = useDark()
const toggleTheme = useToggle(isDark)

const todoStore = useTodoStore()
const showForm = ref(false)
const editingTodo = ref(null)
const searchQuery = ref('')

onMounted(() => {
  todoStore.fetchTodos()
})

const startCreate = () => {
  editingTodo.value = null
  showForm.value = true
}

const startEdit = (todo) => {
  editingTodo.value = todo
  showForm.value = true
}

const cancelForm = () => {
  showForm.value = false
  editingTodo.value = null
}

const handleCreated = async () => {
  showForm.value = false
  editingTodo.value = null
  await todoStore.fetchTodos()
}

const handleUpdate = async (todoData) => {
  try {
    await todoStore.updateTodo(editingTodo.value.id, todoData)
    showForm.value = false
    editingTodo.value = null
    await todoStore.fetchTodos()
  } catch (err) {
    console.error('Failed to update todo:', err)
  }
}

const handleDelete = async (id) => {
  if (!confirm('Are you sure you want to delete this todo?')) {
    return
  }
  
  try {
    await todoStore.deleteTodo(id)
  } catch (err) {
    console.error('Failed to delete todo:', err)
  }
}

const handleToggleComplete = async (id) => {
  await todoStore.toggleComplete(id)
}

const filteredTodos = () => {
  if (!searchQuery.value.trim()) {
    return todoStore.todos
  }
  
  const query = searchQuery.value.toLowerCase()
  return todoStore.todos.filter(todo => 
    todo.title.toLowerCase().includes(query) ||
    (todo.description && todo.description.toLowerCase().includes(query))
  )
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric',
    year: 'numeric'
  })
}

const pendingCount = computed(() => {
  return todoStore.todos.filter(t => !t.completed).length
})
</script>

<template>
  <div class="todo-list">
    <!-- Header -->
    <header class="header">
      <div class="header-content">
        <h1>Tasks</h1>
        <p v-if="pendingCount > 0" class="subtitle">{{ pendingCount }} {{ pendingCount === 1 ? 'task' : 'tasks' }} remaining</p>
      </div>
      <div class="header-actions">
        <button @click="toggleTheme()" class="theme-toggle" :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'">
          {{ isDark ? 'Light' : 'Dark' }}
        </button>
        <button @click="startCreate" class="btn-primary">+ Add Task</button>
      </div>
    </header>

    <!-- Search -->
    <div v-if="todoStore.todos.length > 0" class="search-bar">
      <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <circle cx="11" cy="11" r="8"/>
        <path d="m21 21-4.35-4.35"/>
      </svg>
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="Search tasks..."
        class="search-input"
      />
    </div>

    <!-- Form -->
    <div v-if="showForm" class="form-section">
      <TodoForm 
        :editing-todo="editingTodo"
        @submit="handleUpdate"
        @created="handleCreated"
        @cancel="cancelForm"
      />
    </div>

    <!-- Loading -->
    <div v-else-if="todoStore.loading" class="loading">
      <div class="spinner"></div>
      <p>Loading tasks...</p>
    </div>

    <!-- Empty state -->
    <div v-else-if="filteredTodos().length === 0" class="empty-state">
      <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/>
        <path d="M9 3a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 3v4h6V3"/>
        <path d="M12 11v6M9 14h6"/>
      </svg>
      <p class="empty-text">No tasks yet</p>
      <button @click="startCreate" class="btn-primary">Add your first task</button>
    </div>

    <!-- Todo list -->
    <div v-else class="todo-container">
      <ul class="todo-list-inner">
        <li 
          v-for="todo in filteredTodos()" 
          :key="todo.id"
          class="todo-item"
          :class="{ 'completed': todo.completed }"
          @mouseenter="$event.currentTarget.classList.add('hover')"
          @mouseleave="$event.currentTarget.classList.remove('hover')"
        >
          <div class="todo-checkbox">
            <input 
              type="checkbox" 
              :checked="todo.completed"
              @change="handleToggleComplete(todo.id)"
              :id="`todo-${todo.id}`"
            />
            <label :for="`todo-${todo.id}`"></label>
          </div>
          
          <div class="todo-content">
            <h3 class="todo-title">{{ todo.title }}</h3>
            <p v-if="todo.description" class="todo-description">{{ todo.description }}</p>
          </div>

          <div class="todo-meta">
            <span class="todo-date">{{ formatDate(todo.created_at) }}</span>
          </div>

          <div class="todo-actions">
            <button @click="startEdit(todo)" class="btn-icon" title="Edit">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </button>
            <button @click="handleDelete(todo.id)" class="btn-icon danger" title="Delete">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                <line x1="8" y1="6" x2="8" y2="16"/>
                <line x1="16" y1="6" x2="16" y2="16"/>
              </svg>
            </button>
          </div>
        </li>
      </ul>
    </div>

    <!-- Error -->
    <div v-if="todoStore.error" class="error-banner">
      <p>{{ todoStore.error }}</p>
      <button @click="todoStore.fetchTodos()" class="btn-secondary">Retry</button>
    </div>
  </div>
</template>

<style scoped>
.todo-list {
  max-width: 720px;
  margin: 0 auto;
  padding: var(--space-3xl) var(--space-lg);
}

/* Header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-2xl);
  gap: var(--space-xl);
}

.header-content {
  flex: 1;
}

.header h1 {
  color: var(--color-text-primary);
  margin-bottom: var(--space-xs);
}

.subtitle {
  color: var(--color-text-secondary);
  font-size: var(--font-body-sm);
}

.header-actions {
  display: flex;
  gap: var(--space-md);
  align-items: center;
  flex-shrink: 0;
}

/* Search */
.search-bar {
  position: relative;
  margin-bottom: var(--space-xl);
}

.search-icon {
  position: absolute;
  left: var(--space-md);
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: var(--color-text-tertiary);
}

.search-input {
  width: 100%;
  padding: var(--space-md) calc(var(--space-md) + 24px);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  color: var(--color-text-primary);
  font-size: var(--font-body);
  transition: all 0.2s var(--ease-out-expo);
}

.search-input:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px color-mix(in oklch, var(--color-accent) 15%, transparent);
}

.search-input::placeholder {
  color: var(--color-text-tertiary);
}

/* Form section */
.form-section {
  margin-bottom: var(--space-xl);
  animation: slideDown 0.3s var(--ease-out-expo);
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Loading */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-3xl) 0;
  color: var(--color-text-secondary);
}

.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: var(--space-3xl) 0;
}

.empty-icon {
  width: 48px;
  height: 48px;
  color: var(--color-text-tertiary);
  margin-bottom: var(--space-md);
}

.empty-text {
  color: var(--color-text-secondary);
  margin-bottom: var(--space-lg);
}

/* Todo list */
.todo-container {
  animation: fadeIn 0.4s var(--ease-out-expo);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.todo-list-inner {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.todo-item {
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  gap: var(--space-md);
  padding: var(--space-lg);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  transition: all 0.2s var(--ease-out-expo);
}

.todo-item:hover {
  border-color: color-mix(in oklch, var(--color-accent) 30%, var(--color-border));
  box-shadow: 0 4px 16px color-mix(in oklch, var(--color-text-primary) 8%, transparent);
}

.todo-item.completed .todo-title {
  text-decoration: line-through;
  color: var(--color-text-tertiary);
}

/* Checkbox */
.todo-checkbox {
  position: relative;
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.todo-checkbox input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.todo-checkbox label {
  display: block;
  width: 100%;
  height: 100%;
  border: 2px solid var(--color-border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.2s var(--ease-out-expo);
}

.todo-checkbox input:checked + label {
  background: var(--color-accent);
  border-color: var(--color-accent);
}

.todo-checkbox label::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(0);
  width: 10px;
  height: 6px;
  border-left: 2px solid white;
  border-bottom: 2px solid white;
  transform-origin: center;
  transition: transform 0.15s var(--ease-out-expo);
}

.todo-checkbox input:checked + label::after {
  transform: translate(-50%, -50%) rotate(-45deg) scale(1);
}

/* Content */
.todo-content {
  min-width: 0;
}

.todo-title {
  font-family: var(--font-display);
  font-size: 1.125rem;
  font-weight: 500;
  color: var(--color-text-primary);
  margin-bottom: var(--space-xs);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.todo-description {
  font-size: var(--font-body-sm);
  color: var(--color-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Meta */
.todo-meta {
  flex-shrink: 0;
}

.todo-date {
  font-size: var(--font-body-sm);
  color: var(--color-text-tertiary);
}

/* Actions */
.todo-actions {
  display: flex;
  gap: var(--space-xs);
  flex-shrink: 0;
  opacity: 0;
  transition: opacity 0.2s var(--ease-out-expo);
}

.todo-item:hover .todo-actions {
  opacity: 1;
}

.btn-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: transparent;
  border: none;
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.2s var(--ease-out-expo);
}

.btn-icon svg {
  width: 18px;
  height: 18px;
}

.btn-icon:hover {
  background: var(--color-border);
  color: var(--color-text-primary);
}

.btn-icon.danger:hover {
  background: color-mix(in oklch, var(--color-danger) 20%, transparent);
  color: var(--color-danger);
}

/* Buttons */
.btn-primary {
  padding: var(--space-md) var(--space-lg);
  background: var(--color-accent);
  border: none;
  border-radius: var(--radius-md);
  color: white;
  font-family: inherit;
  font-size: var(--font-body);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s var(--ease-out-expo);
}

.btn-primary:hover {
  background: var(--color-accent-hover);
  transform: translateY(-1px);
}

.btn-secondary {
  padding: var(--space-sm) var(--space-md);
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s var(--ease-out-expo);
}

.btn-secondary:hover {
  background: var(--color-surface);
  border-color: var(--color-text-tertiary);
}

/* Error banner */
.error-banner {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md) var(--space-lg);
  background: color-mix(in oklch, var(--color-danger) 10%, var(--color-surface));
  border: 1px solid color-mix(in oklch, var(--color-danger) 30%, var(--color-border));
  border-radius: var(--radius-lg);
  margin-top: var(--space-lg);
}

.error-banner p {
  margin: 0;
  color: var(--color-danger);
  font-size: var(--font-body-sm);
}

/* Responsive */
@media (max-width: 640px) {
  .todo-list {
    padding: var(--space-lg) var(--space-md);
  }

  .header {
    flex-direction: column;
    gap: var(--space-md);
  }

  .header-actions {
    width: 100%;
    justify-content: space-between;
  }

  .todo-item {
    grid-template-columns: auto 1fr;
    gap: var(--space-md);
  }

  .todo-meta {
    display: none;
  }

  .todo-actions {
    opacity: 1;
    position: absolute;
    top: var(--space-md);
    right: var(--space-md);
  }

  .todo-item {
    position: relative;
  }
}
</style>
