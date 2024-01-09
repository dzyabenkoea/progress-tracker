<script setup>
import './assets/main.css'
import { onMounted, ref } from 'vue'
import { PlusIcon } from '@heroicons/vue/24/outline'
import TrackerElement from '@/components/TrackerElement.vue'
import mockTrackers from '@/mockData/trackers'

const trackers = ref(structuredClone(mockTrackers))

function getTracker(tracker) {
  return trackers.value.find((tr) => tr.id === tracker.id)
}

function addSuccess(tracker) {
  getTracker(tracker).points.push(true)
}

function addFailure(tracker) {
  getTracker(tracker).points.push(false)
}

function removeLastCommit(tracker) {
  getTracker(tracker).points.pop()
}

function addTracker() {
  trackers.value.push({
    id: Math.random() * 1000,
    name: 'Новый трекер',
    points: []
  })
}

function removeTracker(tracker) {
  trackers.value = trackers.value.filter((el) => el.id !== tracker.id)
}

onMounted(async () => {
  const response = await fetch('http://127.0.0.1:8000/api/trackers', { method: 'GET' })
  if (response.status === 200) {
    trackers.value = await response.json()
  } else {
    trackers.value = []
  }
})
</script>
<template>
  <div class="z-10 h-screen w-full bg-sky-950">
    <div class="max-w-2xl p-2">
      <div class="flex flex-col gap-2">
        <template v-for="tracker in trackers">
          <TrackerElement
            :tracker="tracker"
            @add-success="addSuccess(tracker)"
            @add-failure="addFailure(tracker)"
            @remove-last-commit="removeLastCommit(tracker)"
            @remove="removeTracker(tracker)"
          />
        </template>
      </div>
      <div class="flex justify-center">
        <button class="mt-3 w-fit rounded-full bg-sky-900 p-3 text-sky-300" @click="addTracker">
          <PlusIcon class="w-4"></PlusIcon>
        </button>
      </div>
    </div>
  </div>
  <div class="absolute top-0 left-0 z-20 flex h-full w-full items-center justify-center bg-black/40">
    <div class="relative max-w-2xl overflow-hidden rounded border border-sky-900 p-4">
      <p class="text-sky-300">123</p>
      <button class="rounded bg-sky-900 px-4 py-2 text-sky-300 transition-colors hover:bg-sky-800">Добавить</button>
      <div class="absolute top-0 left-0 -z-10 h-full w-full bg-sky-900/20 backdrop-blur-sm"></div>
    </div>
  </div>
</template>