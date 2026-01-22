<script setup>
import { ref, computed } from 'vue'

const STATUS_CONFIG = {
  TT: { label: 'Télétravail', color: 'bg-green-100', border: 'border-green-500', text: 'text-green-800' },
  R: { label: 'Réunion', color: 'bg-blue-100', border: 'border-blue-500', text: 'text-blue-800' },
  CM: { label: 'Congé maternité', color: 'bg-pink-100', border: 'border-pink-500', text: 'text-pink-800' },
  MI: { label: 'Mission', color: 'bg-yellow-100', border: 'border-yellow-500', text: 'text-yellow-800' },
  P: { label: 'Permission', color: 'bg-purple-100', border: 'border-purple-500', text: 'text-purple-800' },
  M: { label: 'Maladie', color: 'bg-red-100', border: 'border-red-500', text: 'text-red-800' },
  F: { label: 'Formation', color: 'bg-indigo-100', border: 'border-indigo-500', text: 'text-indigo-800' },
  REC: { label: 'Récupération', color: 'bg-teal-100', border: 'border-teal-500', text: 'text-teal-800' },
  SS: { label: 'Sur site', color: 'bg-gray-100', border: 'border-gray-500', text: 'text-gray-800' }
}

const currentDate = ref(new Date())
const selectedDate = ref(new Date())


const events = ref([])
const showModal = ref(false)
const newEvent = ref({
  status: 'TT',
  start_time: '',
  end_time: '',
  description: ''
})

const addEvent = () => {
  if (!newEvent.value.start_time || !newEvent.value.end_time || !newEvent.value.description) return

  events.value.push({
    id: Date.now(),
    date: selectedDate.value.toISOString().split('T')[0], 
    ...newEvent.value
  })

  newEvent.value = { status: 'TT', start_time: '', end_time: '', description: '' }
  showModal.value = false
}

const eventsOfDay = computed(() => {
  const selected = selectedDate.value.toISOString().split('T')[0]
  return events.value.filter(e => e.date === selected)
})

const getHourFromTime = (time) => Number(time.split(':')[0])
const getMinutesFromTime = (time) => Number(time.split(':')[1])

const getEventStyle = (event) => {
  const startHour = getHourFromTime(event.start_time)
  const startMin = getMinutesFromTime(event.start_time)
  const endHour = getHourFromTime(event.end_time)
  const endMin = getMinutesFromTime(event.end_time)

  const top = (startMin / 60) * 80
  const height =
    ((endHour + endMin / 60) - (startHour + startMin / 60)) * 80

  return {
    top: `${top}px`,
    height: `${height}px`
  }
}



const daysOfWeek = ['L', 'M', 'M', 'J', 'V', 'S', 'D']

const hours = Array.from({ length: 24 }, (_, i) => i)

const viewOptionSelected = ref('dayView')
const isOpen = ref(false)

const viewOptions = [
  { valueOption: 'dayView', label: 'Vue du jour' },
  { valueOption: 'monthView', label: 'Vue du mois' },
  { valueOption: 'yearView', label: "Vue de l'année" }
]

const selectedLabel = () => viewOptions.find(o => o.valueOption === viewOptionSelected.value)?.label



const formatHour = (hour) => {
  return `${hour.toString().padStart(2, '0')}:00`
}


const getDaysInMonth = (date) => {
  const year = date.getFullYear()
  const month = date.getMonth()
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)

  const daysInMonth = lastDay.getDate()
  const startingDay = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1
  const days = []

  const prevMonthLastDay = new Date(year, month, 0).getDate()
  for (let i = startingDay - 1; i >= 0; i--) {
    days.push({ day: prevMonthLastDay - i, isCurrentMonth: false })
  }

  for (let i = 1; i <= daysInMonth; i++) {
    days.push({ day: i, isCurrentMonth: true })
  }

  while (days.length < 42) {
    days.push({ day: days.length - daysInMonth - startingDay + 1, isCurrentMonth: false })
  }

  return days
}

const days = computed(() => getDaysInMonth(currentDate.value))

const dayClass = (dayObj) => {
  const today = new Date()

  const isToday =
    dayObj.day === today.getDate() &&
    dayObj.isCurrentMonth &&
    currentDate.value.getMonth() === today.getMonth() &&
    currentDate.value.getFullYear() === today.getFullYear()

  const isSelected =
    dayObj.day === selectedDate.value.getDate() &&
    dayObj.isCurrentMonth &&
    currentDate.value.getMonth() === selectedDate.value.getMonth() &&
    currentDate.value.getFullYear() === selectedDate.value.getFullYear()

  return [
    !dayObj.isCurrentMonth && 'text-gray-300',
    dayObj.isCurrentMonth && 'text-gray-900',
    isToday && 'text-indigo-600 border border-indigo-600 font-semibold',
    isSelected && 'bg-indigo-600 text-white',
    dayObj.isCurrentMonth && !isToday && !isSelected && 'hover:bg-gray-100',
  ]
}

</script>

<template>
  <div class="flex h-195 bg-gray-50">
    <div class="flex-1 bg-white border-r border-gray-200">
      <div class="border-b border-gray-200 p-6">
        <div class="flex items-center justify-between mb-2">
          <div>
            <h1 class="text-2xl font-semibold text-gray-900">
              {{ selectedDate.toLocaleDateString('fr-FR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                timeZone: 'Indian/Antananarivo'
              }) }}
            </h1>

            <p class="text-sm text-gray-500">
              {{ selectedDate.toLocaleDateString('fr-FR', {
                weekday: 'long',
                timeZone: 'Indian/Antananarivo'
              }) }}
            </p>

          </div>

          <div class="flex items-center gap-3">
            <button @click="selectedDate = new Date()"
              class="px-4 py-2 text-sm font-medium border rounded border-gray-300 hover:bg-gray-50">
              Today
            </button>


            <div class="relative w-40 text-gray-600">
              <button @click="isOpen = !isOpen"
                class="w-full flex justify-between items-center px-4 py-2 text-sm bg-white border border-gray-300 rounded-lg shadow-sm ">
                {{ selectedLabel() }}
              </button>
              <ul v-if="isOpen"
                class="absolute z-10 mt-1 w-full bg-white border border-gray-200 rounded-lg shadow-lg max-h-48 overflow-auto">
                <li v-for="option in viewOptions" :key="option.valueOption"
                  @click="viewOptionSelected = option.valueOption; isOpen = false"
                  class="px-4 py-2 text-sm cursor-pointer hover:bg-sky-100"
                  :class="{ 'bg-sky-50 text-sky-600 font-medium': viewOptionSelected === option.valueOption }">
                  {{ option.label }}
                </li>
              </ul>
            </div>

            <button @click="showModal = true"
              class="flex items-center gap-2 px-4 py-2 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
              Add event
            </button>
          </div>
        </div>
      </div>

      <!-- Time slots -->
      <div class="overflow-y-auto" style="height: calc(100% - 120px)">
        <div class="relative">
          <div v-for="hour in hours" :key="hour" class="flex border-b border-gray-100" style="height: 80px">
            <div class="w-20 shrink-0 text-xs text-gray-500 text-right pr-4 pt-1">
              {{ formatHour(hour) }}
            </div>

            <!-- 👇 ZONE EVENTS (C’EST ÇA QUI MANQUAIT) -->
            <div class="flex-1 relative">
              <div v-for="event in eventsOfDay.filter(e => getHourFromTime(e.start_time) === hour)" :key="event.id"
                class="absolute left-2 right-2 rounded-lg p-3 border-l-4" :class="[
                  STATUS_CONFIG[event.status].color,
                  STATUS_CONFIG[event.status].border
                ]" :style="getEventStyle(event)">
                <div class="text-xs font-semibold" :class="STATUS_CONFIG[event.status].text">
                  {{ event.start_time.slice(0, 5) }} - {{ event.end_time.slice(0, 5) }}
                </div>

                <div class="text-sm font-semibold">
                  {{ STATUS_CONFIG[event.status].label }}
                </div>

                <div class="text-xs opacity-80">
                  {{ event.description }}
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Right side - Month view -->
    <div class="w-96 bg-white p-6">
      <div class="flex items-center justify-between mb-6">

        <h2 class="text-lg font-semibold">
          {{ currentDate.toLocaleDateString('fr-FR', {
            month: 'long',
            year: 'numeric',
            timeZone: 'Indian/Antananarivo'
          }) }}
        </h2>

      </div>

      <!-- Calendar grid -->
      <div class="grid grid-cols-7 gap-1">
        <div v-for="day in daysOfWeek" :key="day" class="text-center text-xs font-medium text-gray-500 py-2">
          {{ day }}
        </div>

        <button v-for="(dayObj, index) in days" :key="index" @click="dayObj.isCurrentMonth &&
          (selectedDate = new Date(
            currentDate.getFullYear(),
            currentDate.getMonth(),
            dayObj.day
          ))" class="aspect-square flex items-center justify-center text-sm rounded-lg" :class="dayClass(dayObj)">
          {{ dayObj.day }}
        </button>
      </div>
    </div>

    <div v-if="showModal" class="fixed inset-0 bg-black/2 backdrop-blur-[5px] bg-opacity-40 flex items-center justify-center z-50">
      <div class="bg-white shadow-lg p-6 rounded-lg w-96">
        <h2 class="text-lg font-semibold mb-4">Ajouter un événement</h2>

        <div class="mb-2">
          <label class="block text-sm mb-1">Statut</label>
          <select v-model="newEvent.status" class="w-full border rounded px-2 py-1">
            <option v-for="(s, key) in STATUS_CONFIG" :key="key" :value="key">
              {{ s.label }}
            </option>
          </select>
        </div>

        <div class="mb-2">
          <label class="block text-sm mb-1">Heure début</label>
          <input type="time" v-model="newEvent.start_time" class="w-full border rounded px-2 py-1" />
        </div>

        <div class="mb-2">
          <label class="block text-sm mb-1">Heure fin</label>
          <input type="time" v-model="newEvent.end_time" class="w-full border rounded px-2 py-1" />
        </div>

        <div class="mb-4">
          <label class="block text-sm mb-1">Description</label>
          <input type="text" v-model="newEvent.description" class="w-full border rounded px-2 py-1" />
        </div>

        <div class="flex justify-end gap-2">
          <button @click="showModal = false" class="px-4 py-2 border rounded hover:bg-gray-100">Annuler</button>
          <button @click="addEvent"
            class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700">Ajouter</button>
        </div>
      </div>
    </div>

  </div>
</template>