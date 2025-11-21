<script setup>
import { inject, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = defineProps({
  path: {
    type: Array,
    required: true
  },
  strokeWeight: {
    type: Number,
    default: 2
  },
  strokeColor: {
    type: String,
    default: '#2563eb'
  },
  strokeOpacity: {
    type: Number,
    default: 0.8
  },
  strokeStyle: {
    type: String,
    default: 'solid'
  },
  fillColor: {
    type: String,
    default: '#2563eb'
  },
  fillOpacity: {
    type: Number,
    default: 0.3
  }
})

const mapRef = inject('mapRef')
const polygon = ref(null)

const toLatLngPath = () => {
  if (!window?.kakao?.maps) return []
  return props.path.map((coord) => new window.kakao.maps.LatLng(coord.lat, coord.lng))
}

const upsertPolygon = () => {
  if (!mapRef?.value || !window?.kakao?.maps || props.path.length === 0) return
  const paths = [toLatLngPath()]

  if (polygon.value) {
    polygon.value.setOptions({
      strokeWeight: props.strokeWeight,
      strokeColor: props.strokeColor,
      strokeOpacity: props.strokeOpacity,
      strokeStyle: props.strokeStyle,
      fillColor: props.fillColor,
      fillOpacity: props.fillOpacity
    })
    polygon.value.setPath(paths)
  } else {
    polygon.value = new window.kakao.maps.Polygon({
      map: mapRef.value,
      path: paths,
      strokeWeight: props.strokeWeight,
      strokeColor: props.strokeColor,
      strokeOpacity: props.strokeOpacity,
      strokeStyle: props.strokeStyle,
      fillColor: props.fillColor,
      fillOpacity: props.fillOpacity
    })
  }
}

watch(
  () => [
    props.path,
    props.strokeWeight,
    props.strokeColor,
    props.strokeOpacity,
    props.strokeStyle,
    props.fillColor,
    props.fillOpacity
  ],
  () => {
    upsertPolygon()
  },
  { deep: true }
)

onMounted(() => {
  upsertPolygon()
})

onBeforeUnmount(() => {
  if (polygon.value) {
    polygon.value.setMap(null)
    polygon.value = null
  }
})
</script>
