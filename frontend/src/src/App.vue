<script setup>
import './assets/main.css'
import { onMounted, ref } from 'vue'
import { PlusIcon } from '@heroicons/vue/24/outline'
import TrackerElement from '@/components/TrackerElement.vue'
/** @type Tracker */
import mockTrackers from '@/mockData/trackers'

/**
 * @typedef {Object} Tracker
 * @property {string} name
 * @property {number} id
 * @property {boolean[]} points
 */
/**
 * @type Ref<Tracker[]>
 */
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
        <TransitionGroup appear enter-active-class="transition" enter-from-class="opacity-0" enter-to-class="opacity-1"
        leave-active-class="relative transition" leave-from-class="opacity-1" leave-to-class="opacity-0">
          <template :key="tracker.id" v-for="tracker in trackers">
            <TrackerElement
              :tracker="tracker"
              @add-success="addSuccess(tracker)"
              @add-failure="addFailure(tracker)"
              @remove-last-commit="removeLastCommit(tracker)"
              @remove="removeTracker(tracker)"
            />
          </template>
        </TransitionGroup>
      </div>
      <div class="flex justify-center">
        <button class="mt-3 w-fit rounded-full bg-sky-900 p-3 text-sky-300" @click="addTracker">
          <PlusIcon class="w-4"></PlusIcon>
        </button>
      </div>
    </div>
  </div>
</template>