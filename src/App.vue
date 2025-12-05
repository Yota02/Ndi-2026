<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import SpriteAnimation from './components/TuxAnimation.vue'

const currentEmotion = ref('happy')

const handleScroll = () => {
  if (window.scrollY > 500) {
    currentEmotion.value = 'sad'
  } else {
    currentEmotion.value = 'happy'
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <SpriteAnimation
    :x="100"
    :y="100"
    :width="300"
    :height="300"
    :emotion="currentEmotion"
    :hoverEmotion="'happy'"
  />
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
  font-family: Arial, sans-serif;
}

.animation-area {
  position: relative;
  height: 500px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  margin-bottom: 2rem;
  backdrop-filter: blur(10px);
}

.controls {
  background: white;
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

h2 {
  color: #333;
  margin-bottom: 1.5rem;
  text-align: center;
}

.toggle-container {
  margin-bottom: 2rem;
  display: flex;
  justify-content: center;
}

.toggle {
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
}

.toggle input[type='checkbox'] {
  width: 50px;
  height: 26px;
  appearance: none;
  background: #ccc;
  border-radius: 13px;
  position: relative;
  cursor: pointer;
  transition: background 0.3s;
}

.toggle input[type='checkbox']:checked {
  background: #667eea;
}

.toggle input[type='checkbox']::before {
  content: '';
  position: absolute;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: white;
  top: 2px;
  left: 2px;
  transition: transform 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.toggle input[type='checkbox']:checked::before {
  transform: translateX(24px);
}

.toggle-label {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.toggle-label small {
  color: #667eea;
  font-weight: 600;
}

.select-container {
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

select {
  padding: 0.5rem;
  font-size: 1rem;
  border: 2px solid #667eea;
  border-radius: 10px;
  background: white;
  color: #667eea;
  cursor: pointer;
}

select:focus {
  outline: none;
  box-shadow: 0 0 5px rgba(102, 126, 234, 0.5);
}

.button-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

button {
  padding: 1rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: #667eea;
  background: white;
  border: 2px solid #667eea;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  background: #667eea;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

button.active {
  background: #667eea;
  color: white;
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}
</style>
