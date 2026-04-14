<script setup>
import { RouterView } from 'vue-router'
import { watch } from 'vue'
import { useDark, useToggle } from '@vueuse/core'
import './style.css'

const isDark = useDark()
const toggleTheme = useToggle(isDark)

// Apply theme class to html element
watch(isDark, (value) => {
  if (value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
})

// Initialize theme
if (isDark.value) {
  document.documentElement.classList.add('dark')
}
</script>

<template>
  <div class="app">
    <RouterView />
  </div>
</template>

<style>
/* Base styles are in style.css */
</style>
