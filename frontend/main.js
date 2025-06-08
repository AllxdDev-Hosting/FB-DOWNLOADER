import { createApp } from 'vue'
import App from './App.vue'
import Modal from './components/Modal.vue'
import './index.css'

const app = createApp(App)
app.component('Modal', Modal)
app.mount('#app')
