<script setup>
import "./assets/main.css";
import { onMounted, ref } from "vue";
import { PlusIcon } from "@heroicons/vue/24/outline";
import TrackerElement from "@/components/TrackerElement.vue";

const trackers = ref();

function getTracker(tracker) {
  return trackers.value.find((tr) => tr.id === tracker.id);
}

function addSuccess(tracker) {
  getTracker(tracker).points.push(true);
}

function addFailure(tracker) {
  getTracker(tracker).points.push(false);
}

function removeLastCommit(tracker) {
  getTracker(tracker).points.pop();
}

function addTracker() {
  trackers.value.push({
    id: Math.random() * 1000,
    name: "Новый трекер",
    points: []
  });
}

onMounted(async () => {
  const response = await fetch("http://127.0.0.1:8000/api/trackers", { method: "GET" });
  if (response.status === 200) {
    trackers.value = await response.json()
  } else {
    trackers.value = [];
  }
});
</script>
<template>
  <div class="w-full h-screen bg-sky-950">
    <div class="max-w-2xl p-2">
      <div class="flex flex-col gap-2">
        <template v-for="tracker in trackers">
          <TrackerElement
            :tracker="tracker"
            @add-success="addSuccess(tracker)"
            @add-failure="addFailure(tracker)"
            @remove-last-commit="removeLastCommit(tracker)"
          />
        </template>
      </div>
      <div class="flex justify-center">
        <button class="mt-3 p-3 w-fit bg-sky-900 text-sky-300 rounded-full" @click="addTracker">
          <PlusIcon class="w-4"></PlusIcon>
        </button>
      </div>
    </div>
  </div>
</template>