<script setup>
import { ref, watch } from 'vue'
import { useTodoStore } from '../stores/todoStore.js'

const props = defineProps({
  editingTodo: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel', 'created'])

const todoStore = useTodoStore()

const form = ref({
  title: '',
  description: '',
  completed: false
})

const errors = ref({})

const validateForm = () => {
  errors.value = {}
  
  if (!form.value.title.trim()) {
    errors.value.title = 'Title is required'
    return false
  }
  
  if (form.value.title.length > 200) {
    errors.value.title = 'Title must be less than 200 characters'
    return false
  }
  
  return true
}

const submitForm = async () => {
  if (!validateForm()) return

  const payload = { ...form.value }

  try {
    if (props.editingTodo) {
      await todoStore.updateTodo(props.editingTodo.id, payload)
      emit('submit', payload)
    } else {
      await todoStore.createTodo(payload)
      emit('created')
      resetForm()
    }
  } catch (err) {
    // error handled by store
  }
}

const cancelForm = () => {
  resetForm()
  emit('cancel')
}

const resetForm = () => {
  form.value = { title: '', description: '', completed: false }
  errors.value = {}
}

watch(() => props.editingTodo, (newVal) => {
  if (newVal) {
    form.value = {
      title: newVal.title,
      description: newVal.description || '',
      completed: newVal.completed
    }
  } else {
    resetForm()
  }
}, { immediate: true })
</script>

<template>
  <div class="todo-form">
    <h2>{{ editingTodo ? 'Edit Task' : 'New Task' }}</h2>
    
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="title">Title</label>
        <input 
          id="title" 
          v-model="form.title" 
          placeholder="What needs to be done?"
          :class="{ 'error': errors.title }"
          autocomplete="off"
        />
        <span v-if="errors.title" class="error-message">{{ errors.title }}</span>
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <textarea 
          id="description" 
          v-model="form.description" 
          placeholder="Add details (optional)"
          rows="3"
        ></textarea>
      </div>

      <div class="form-actions">
        <button type="submit" :disabled="todoStore.loading || !form.title.trim()">
          {{ todoStore.loading ? 'Saving...' : (editingTodo ? 'Update' : 'Create') }}
        </button>
        <button type="button" @click="cancelForm">Cancel</button>
      </div>
    </form>

    <div v-if="todoStore.error" class="error-banner">
      {{ todoStore.error }}
    </div>
  </div>
</template>

<style scoped>
.todo-form {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-xl);
}

h2 {
  font-family: var(--font-display);
  color: var(--color-text-primary);
  margin-bottom: var(--space-lg);
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: var(--space-md);
}

label {
  display: block;
  font-size: var(--font-body-sm);
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-xs);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

input[type="text"],
textarea {
  width: 100%;
  padding: var(--space-md);
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-family: inherit;
  font-size: var(--font-body);
  transition: all 0.2s var(--ease-out-expo);
}

input[type="text"]:focus,
textarea:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px color-mix(in oklch, var(--color-accent) 15%, transparent);
}

input.error,
textarea.error {
  border-color: var(--color-danger);
}

.error-message {
  display: block;
  margin-top: var(--space-xs);
  color: var(--color-danger);
  font-size: var(--font-body-sm);
}

.form-actions {
  display: flex;
  gap: var(--space-md);
  margin-top: var(--space-lg);
  padding-top: var(--space-lg);
  border-top: 1px solid var(--color-border);
}

button[type="submit"] {
  padding: var(--space-md) var(--space-xl);
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

button[type="submit"]:hover:not(:disabled) {
  background: var(--color-accent-hover);
}

button[type="submit"]:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

button[type="button"] {
  padding: var(--space-md) var(--space-xl);
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s var(--ease-out-expo);
}

button[type="button"]:hover {
  background: var(--color-bg);
  border-color: var(--color-text-tertiary);
}

.error-banner {
  margin-top: var(--space-md);
  padding: var(--space-md);
  background: color-mix(in oklch, var(--color-danger) 10%, var(--color-bg));
  border: 1px solid color-mix(in oklch, var(--color-danger) 30%, var(--color-border));
  border-radius: var(--radius-md);
  color: var(--color-danger);
  font-size: var(--font-body-sm);
}

@media (max-width: 640px) {
  .todo-form {
    padding: var(--space-lg);
  }

  .form-actions {
    flex-direction: column;
  }

  button {
    width: 100%;
  }
}
</style>
