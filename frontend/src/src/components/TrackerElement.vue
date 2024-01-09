<script setup lang="ts">
import { ArrowUturnLeftIcon, CheckIcon, MinusIcon } from '@heroicons/vue/24/outline'
import { computed, onMounted, ref, watch } from 'vue'

const props = defineProps<{ tracker: { name: string; points: boolean[] } }>()
const emits = defineEmits(['add-success', 'add-failure', 'remove-last-commit', 'remove'])
const titleIsEditable = ref(false)

const loss = computed(() => {
  const losses = props.tracker.points.filter((el) => !el)
  return losses.length
})
const wins = computed(() => {
  const wins = props.tracker.points.filter((el) => !!el)
  return wins.length
})
const titleInput = ref<HTMLInputElement>()

const isDragging = ref(false)
const leftPositioning = computed(() => {
  const maxOffset = 100
  const newPositionStyling =
    currentOffsetDiff.value <= maxOffset ? currentOffsetDiff.value : maxOffset
  console.log('Сдвиг:', newPositionStyling)

  return `-${newPositionStyling}px`
})

const trackerContainer = ref()

let [offsetX, offsetY] = [0, 0]
let currentOffsetDiff = ref(0)

function onTitleClick() {
  titleIsEditable.value = true
  setTimeout(() => {
    titleInput.value.focus()
    titleInput.value.select()
  })
}

function startDrag(event: DragEvent) {
  console.log('drag')
  isDragging.value = true

  offsetX = event.offsetX
  offsetY = event.offsetY
  console.log(offsetX, offsetY)
}

function onTrackerDrop() {
  console.log('drop')
  isDragging.value = false

  if (currentOffsetDiff.value > 60) {
    currentOffsetDiff.value = 100
  } else {
    currentOffsetDiff.value = 0
  }
}

function onMouseMove(event: MouseEvent) {
  console.log('onMouseMove')
  console.log(offsetX, offsetY)
  console.log(event.offsetX, event.offsetY)
  currentOffsetDiff.value = offsetX - event.offsetX
}

watch(isDragging, () => {
  if (isDragging.value === true) trackerContainer.value.addEventListener('mousemove', onMouseMove)
  else trackerContainer.value.removeEventListener('mousemove', onMouseMove)
})

onMounted(() => {
  document.addEventListener('mouseup', () => {
    onTrackerDrop()
  })
})
</script>

<template>
  <div class="relative" ref="trackerContainer" @mousedown="startDrag" @dragstart.prevent>
    <article
      class="z-20 relative rounded-md px-3 py-2 flex flex-col gap-2 shadow bg-sky-900 bg-gradient-to-b from-sky-800 to-sky-900"
      :style="{ left: leftPositioning }"
    >
      <div class="flex">
        <div class="flex flex-col grow gap-2 pr-2">
          <p
            v-if="!titleIsEditable"
            @click="onTitleClick"
            class="bg-transparent border-none outline-none text-sky-300 text-md font-semibold"
          >
            {{ tracker.name }}
          </p>
          <input
            ref="titleInput"
            v-show="titleIsEditable"
            v-model="tracker.name"
            class="bg-transparent border-none outline-none text-sky-300 text-md font-semibold"
            @blur="titleIsEditable = false"
            @keyup="
              (event) => {
                const codes = ['Escape', 'Enter', 'NumpadEnter']
                if (codes.find((el) => el === event.code)) {
                  titleInput.blur()
                }
              }
            "
          />
          <p class="text-sky-400 text-sm">
            Результат: {{ wins }} / <span class="text-sky-600">{{ loss }}</span>
          </p>
          <div class="flex gap-1 flex-wrap">
            <TransitionGroup
              enter-from-class="opacity-0 scale-[400%]"
              enter-active-class="transform duration-200"
              enter-to-class="opacity-100 scale-100"
              leave-from-class="opacity-100 scale-scale-100"
              leave-active-class="transform duration-200"
              leave-to-class="opacity-0 scale-0"
            >
              <div
                :key="index"
                v-for="(point, index) in tracker.points"
                class="rounded w-3 h-3 shrink-0 border-sky-400 border"
                :class="{
                  'bg-sky-500 shadow shadow-sky-600': point === true,
                  '': point === false
                }"
              ></div>
            </TransitionGroup>
          </div>
        </div>
        <div class="pl-2 border-l border-sky-800 flex flex-col gap-1 items-center">
          <button @click="emits('add-success')">
            <CheckIcon class="text-sky-500 w-6"></CheckIcon>
          </button>
          <button @click="emits('add-failure')">
            <MinusIcon class="text-sky-500 w-6"></MinusIcon>
          </button>
          <button @click="emits('remove-last-commit')">
            <ArrowUturnLeftIcon class="text-sky-500 w-6"></ArrowUturnLeftIcon>
          </button>
        </div>
      </div>
    </article>
    <div
      class="z-10 p-4 bg-red-500 rounded-md absolute right-0 top-0 text-white h-full flex items-center cursor-pointer"
      @click="emits('remove')"
    >
      <p>Удалить</p>
    </div>
  </div>
</template>

<style scoped></style>