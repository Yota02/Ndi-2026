<template>
  <div class="chat-widget">

    <transition name="slide-fade">
      <div v-show="isOpen" class="chat-window">
        <vue-advanced-chat
          style="height: 100%; width: 100%;"

          :current-user-id="currentUserId"
          :room-id="'room_1'"
          :single-room="true"
          :rooms="JSON.stringify(rooms)"
          :messages="JSON.stringify(messages)"
          :message-actions="JSON.stringify(messageActions)"

          :rooms-loaded="true"
          :messages-loaded="messagesLoaded"
          @fetch-messages="fetchMessages"

          :styles="JSON.stringify(customStyles)"

          :show-audio="false"
          :show-files="false"
          :message-sound="false"
          :show-search="false"
          :show-add-room="false"
          @send-message="sendMessage"
        />
      </div>
    </transition>

    <button class="chat-toggle-btn" @click="toggleChat">
      <svg v-if="isOpen" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="6" x2="6" y2="18"></line>
        <line x1="6" y1="6" x2="18" y2="18"></line>
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
      </svg>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { register } from 'vue-advanced-chat'
import axios from 'axios'

register()

// --- Interfaces ---
interface ChatUser { _id: string; username: string; avatar?: string; status?: { state: string; lastChanged: string } }
// AJOUT : typingUsers dans l'interface
interface ChatRoom { roomId: string; roomName: string; avatar: string; users: ChatUser[]; typingUsers?: string[] }
interface ChatMessage { _id: string | number; content: string; senderId: string; username?: string; timestamp: string; date: string; saved?: boolean; distributed?: boolean; seen?: boolean; disableActions?: boolean; disableReactions?: boolean }
interface MessageAction { name: string; title: string }
interface FlaskResponse { content: string; senderId: string }

// --- Styles ---
const customStyles = ref({
  sidemenu: { display: 'none', width: '0px', border: 'none' },
  container: {
    borderRadius: '12px',
    height: '100%',
    minHeight: '100%'
  }
})

// --- États Réactifs ---
const isOpen = ref(false)
const currentUserId = ref<string>('user_1')
const messagesLoaded = ref(false)

const rooms = ref<ChatRoom[]>([
  {
    roomId: 'room_1',
    roomName: 'Barnabé le Bot',
    avatar: 'https://cdn-icons-png.flaticon.com/512/4712/4712035.png',
    users: [{ _id: 'user_1', username: 'Moi' }, { _id: 'bot_id', username: 'Barnabé' }],
    typingUsers: [] // Initialisé à vide
  }
])

const messages = ref<ChatMessage[]>([])
const messageActions = ref<MessageAction[]>([{ name: 'replyMessage', title: 'Répondre' }])

// --- Logique ---

const toggleChat = () => {
  isOpen.value = !isOpen.value
}

const fetchMessages = ({ detail }: any) => {
  setTimeout(() => { messagesLoaded.value = true }, 500)
}

const sendMessage = async (event: any) => {
  const { content, roomId } = event.detail[0]

  // 1. Ajouter le message de l'utilisateur
  const userMessage: ChatMessage = {
    _id: new Date().getTime(),
    content: content,
    senderId: currentUserId.value,
    timestamp: new Date().toString().substring(16, 21),
    date: new Date().toDateString(),
    saved: true, distributed: true, seen: true
  }

  messages.value = [...messages.value, userMessage]

  // 2. Préparer l'historique pour Flask
  const conversationHistory = messages.value.map(msg => {
    return {
      role: msg.senderId === currentUserId.value ? 'user' : 'assistant',
      content: msg.content
    }
  })

  // --- DÉBUT INDICATEUR DE FRAPPE ---
  // On signale que le bot (bot_id) est en train d'écrire dans la room 0
  if (rooms.value[0]) {
    rooms.value[0].typingUsers = ['bot_id']
  }
  // ---------------------------------

  try {
    const response = await axios.post<FlaskResponse>('http://backend-ndi.cluster-ig3.igpolytech.fr/api/chat', {
      history: conversationHistory,
      roomId: roomId
    })

    const botMessage: ChatMessage = {
      _id: new Date().getTime() + 1,
      content: response.data.content,
      senderId: response.data.senderId,
      timestamp: new Date().toString().substring(16, 21),
      date: new Date().toDateString()
    }

    messages.value = [...messages.value, botMessage]

  } catch (error) {
    console.error("Erreur Flask:", error)
    // Optionnel : Ajouter un message d'erreur visible pour l'utilisateur ici
  } finally {
    // --- FIN INDICATEUR DE FRAPPE ---
    // Quoi qu'il arrive (succès ou erreur), on enlève les trois petits points
    if (rooms.value[0]) {
      rooms.value[0].typingUsers = []
    }
  }
}
</script>

<style scoped>
/* Conteneur global */
.chat-widget {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  font-family: 'Segoe UI', sans-serif;
}

/* Fenêtre de chat */
.chat-window {
  width: 480px;
  height: 720px;
  max-height: calc(100vh - 100px);
  margin-bottom: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  overflow: hidden;
  background-color: white;
  display: flex;
  flex-direction: column;
}

/* Force la librairie à prendre 100% */
.chat-window :deep(.vac-container),
.chat-window :deep(.vac-container-scroll),
.chat-window :deep(.vac-room-container) {
  height: 100% !important;
  max-height: 100% !important;
}

/* Bouton Rond */
.chat-toggle-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.chat-toggle-btn:hover {
  transform: scale(1.1);
}

.chat-toggle-btn:active {
  transform: scale(0.95);
}

/* Animation */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease-out;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(20px);
  opacity: 0;
}

/* Mobile */
@media (max-width: 480px) {
  .chat-window {
    width: calc(100vw - 40px);
    height: calc(100vh - 120px);
    position: fixed;
    bottom: 90px;
    right: 20px;
    max-height: none;
  }
}
</style>
