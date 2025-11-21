import { createApp } from 'vue'
import { Vue3KakaoMaps } from 'vue3-kakao-maps'
import { useKakao } from 'vue3-kakao-maps/@utils'
import './style.css'
import App from './App.vue'

const app = createApp(App)

const kakaoKey = import.meta.env.VITE_KAKAO_JS_KEY
if (kakaoKey) {
  useKakao(kakaoKey, { libraries: ['services'] })
} else {
  console.warn('VITE_KAKAO_JS_KEY is not set. Kakao map will not load.')
}

app.use(Vue3KakaoMaps)

app.mount('#app')
