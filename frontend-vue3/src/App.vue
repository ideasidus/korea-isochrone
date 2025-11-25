<script setup>
import { computed, ref } from 'vue'
import axios from 'axios'
import { KakaoMap, KakaoMapMarker } from 'vue3-kakao-maps'
import KakaoPolygon from './components/KakaoPolygon.vue'

const KAKAO_SEARCH_URL = 'https://dapi.kakao.com/v2/local/search/keyword.json'
const kakaoRestKey = import.meta.env.VITE_KAKAO_REST_API_KEY
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL

const DEFAULT_CENTER = { lat: 37.5665, lng: 126.978 } // 서울 시청

const searchQuery = ref('')
const searchResults = ref([])
const isSearching = ref(false)
const searchError = ref('')
const selectedPlace = ref(null)

const cutoffMinutes = ref(30)
const mode = ref('DEFAULT')
const arriveBy = ref(false)
const useCustomTime = ref(false)
const customDate = ref('')
const customTime = ref('')
const backendError = ref('')
const isRequestingIsochrone = ref(false)
const isoFeatures = ref([])

const mapCenter = computed(() => selectedPlace.value ?? DEFAULT_CENTER)
const hasRestKey = computed(() => Boolean(kakaoRestKey))
const hasBackendUrl = computed(() => Boolean(apiBaseUrl))

const fromPlace = computed(() =>
  selectedPlace.value ? `${selectedPlace.value.lat},${selectedPlace.value.lng}` : ''
)

const formattedResults = computed(() =>
  searchResults.value.map((item) => ({
    id: item.id,
    name: item.place_name,
    address: item.road_address_name || item.address_name,
    lat: Number(item.y),
    lng: Number(item.x)
  }))
)

const isoPolygons = computed(() => {
  const palette = ['#2563eb', '#7c3aed', '#ea580c', '#16a34a']
  return isoFeatures.value.flatMap((feature, idx) => {
    const { geometry, properties } = feature
    if (!geometry || !geometry.coordinates) return []
    const fillColor = palette[idx % palette.length]

    if (geometry.type === 'Polygon') {
      return [
        {
          path: geometry.coordinates[0].map(([lng, lat]) => ({ lat, lng })),
          fillColor,
          strokeColor: fillColor,
          label: properties?.time || `${idx + 1}번 영역`
        }
      ]
    }

    if (geometry.type === 'MultiPolygon') {
      return geometry.coordinates.map((ring) => ({
        path: ring[0].map(([lng, lat]) => ({ lat, lng })),
        fillColor,
        strokeColor: fillColor,
        label: properties?.time || `${idx + 1}번 영역`
      }))
    }

    return []
  })
})

const handlePlaceSelect = (place) => {
  selectedPlace.value = { lat: place.lat, lng: place.lng, name: place.name }
  backendError.value = ''
}

const searchPlaces = async () => {
  if (!hasRestKey.value) {
    searchError.value = 'VITE_KAKAO_REST_API_KEY를 .env에 설정해주세요.'
    return
  }

  if (!searchQuery.value.trim()) {
    searchError.value = '검색어를 입력해주세요.'
    return
  }

  searchError.value = ''
  isSearching.value = true

  try {
    const { data } = await axios.get(KAKAO_SEARCH_URL, {
      params: {
        query: searchQuery.value,
        size: 5
      },
      headers: {
        Authorization: `KakaoAK ${kakaoRestKey}`
      }
    })
    searchResults.value = data.documents ?? []
  } catch (error) {
    console.error(error)
    searchError.value = '장소 검색 중 오류가 발생했습니다.'
  } finally {
    isSearching.value = false
  }
}

const requestIsochrone = async () => {
  if (!hasBackendUrl.value) {
    backendError.value = 'VITE_API_BASE_URL을 .env에 설정해주세요.'
    return
  }

  if (!fromPlace.value) {
    backendError.value = '좌표를 먼저 선택해주세요.'
    return
  }

  if (!Number.isFinite(cutoffMinutes.value) || cutoffMinutes.value < 1) {
    backendError.value = 'cutoffMin은 1분 이상의 정수를 입력해주세요.'
    return
  }

  backendError.value = ''
  isRequestingIsochrone.value = true

  try {
    const params = {
      lat: selectedPlace.value.lat,
      lon: selectedPlace.value.lng,
      cutoffMin: Math.round(cutoffMinutes.value),
      arriveBy: arriveBy.value
    }

    if (mode.value !== 'DEFAULT') {
      params.modes = [mode.value]
    }

    if (useCustomTime.value && customDate.value && customTime.value) {
      params.date = customDate.value
      params.time = customTime.value
    }

    const { data } = await axios.get(`${apiBaseUrl}/api/v1/isochrone`, { params })
    isoFeatures.value = data?.features ?? []
  } catch (error) {
    console.error(error)
    backendError.value =
      error.response?.data?.message || 'Isochrone 요청 중 오류가 발생했습니다.'
  } finally {
    isRequestingIsochrone.value = false
  }
}
</script>

<template>
  <div class="page">
    <section class="panel controls">
      <h1>Isochrone Explorer</h1>
      <p class="description">
        카카오 지도에서 좌표를 검색하고, Isochrone API 결과를 폴리곤으로 시각화합니다.
      </p>

      <div class="field">
        <label>장소 검색</label>
        <div class="field__inline">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="예) 서울역"
            @keyup.enter="searchPlaces"
          />
          <button :disabled="isSearching" @click="searchPlaces">
            {{ isSearching ? '검색 중...' : '검색' }}
          </button>
        </div>
        <p v-if="searchError" class="error">{{ searchError }}</p>
      </div>

      <ul v-if="formattedResults.length" class="results">
        <li
          v-for="place in formattedResults"
          :key="place.id"
          :class="{ selected: selectedPlace?.name === place.name }"
          @click="handlePlaceSelect(place)"
        >
          <strong>{{ place.name }}</strong>
          <span>{{ place.address }}</span>
          <small>{{ place.lat.toFixed(6) }}, {{ place.lng.toFixed(6) }}</small>
        </li>
      </ul>

      <div class="field">
        <label>선택된 좌표</label>
        <input type="text" :value="fromPlace" readonly placeholder="좌표를 선택하세요" />
      </div>

      <div class="grid">
        <div class="field">
          <label>cutoffMin (분)</label>
          <input v-model.number="cutoffMinutes" type="number" min="1" max="180" step="5" />
        </div>
        <div class="field">
          <label>mode</label>
          <select v-model="mode">
            <option value="DEFAULT">기본 (WALK+TRANSIT)</option>
            <option value="WALK">WALK</option>
            <option value="TRANSIT">TRANSIT</option>
            <option value="BICYCLE">BICYCLE</option>
            <option value="CAR">CAR</option>
          </select>
        </div>
      </div>

      <div class="grid">
        <div class="field field--inline">
          <label>
            <input v-model="arriveBy" type="checkbox" />
            도착 기준(arriveBy)
          </label>
        </div>
        <div class="field field--inline custom-time-toggle">
          <label>
            <input v-model="useCustomTime" type="checkbox" />
            날짜/시간 지정
          </label>
          <small>날짜는 평일/주말·공휴일 등 GTFS 캘린더를 반영하기 위해 필요합니다.</small>
        </div>
      </div>

      <div class="grid" v-if="useCustomTime">
        <div class="field">
          <label>날짜</label>
          <input v-model="customDate" type="date" />
        </div>
        <div class="field">
          <label>시간</label>
          <input v-model="customTime" type="time" />
        </div>
      </div>

      <button class="primary" :disabled="isRequestingIsochrone" @click="requestIsochrone">
        {{ isRequestingIsochrone ? '요청 중...' : 'Isochrone 요청' }}
      </button>

      <p v-if="backendError" class="error">{{ backendError }}</p>
    </section>

    <section class="panel map">
      <KakaoMap
        class="kakao-map"
        :lat="mapCenter.lat"
        :lng="mapCenter.lng"
        :level="5"
        width="100%"
        height="100%"
        draggable
        zoomable
      >
        <template v-if="selectedPlace">
          <KakaoMapMarker
            :lat="selectedPlace.lat"
            :lng="selectedPlace.lng"
            :info-window="{ content: selectedPlace.name }"
          />
        </template>

        <KakaoPolygon
          v-for="(polygon, idx) in isoPolygons"
          :key="idx"
          :path="polygon.path"
          :stroke-weight="2"
          :stroke-color="polygon.strokeColor"
          :stroke-opacity="0.8"
          stroke-style="solid"
          :fill-color="polygon.fillColor"
          :fill-opacity="0.35"
        />
      </KakaoMap>

      <div v-if="!hasRestKey || !hasBackendUrl" class="helper">
        <p>
          .env 파일에 <code>VITE_KAKAO_JS_KEY</code>,
          <code>VITE_KAKAO_REST_API_KEY</code>,
          <code>VITE_API_BASE_URL</code> 값을 설정한 후 다시 시도하세요.
        </p>
      </div>
    </section>
  </div>
</template>
