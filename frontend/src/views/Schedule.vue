<script setup>
import { ref, computed, onMounted } from 'vue';
import { getAllSchedules } from '../api/schedule';
import MainLayout from '../layouts/MainLayout.vue';
import { getAllUsers } from '../api/auth';

const users = ref([]);

const today = new Date()
const currentYear = ref(today.getFullYear())
const currentMonth = ref(today.getMonth())
const monthNames = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
const weekDays = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam']
const todayCell = ref(null)

const daysInMonth = computed(() => new Date(currentYear.value, currentMonth.value + 1, 0).getDate())

const formatDate = (year, month, day) => {
  const m = String(month + 1).padStart(2, '0')
  const d = String(day).padStart(2, '0')
  return `${year}-${m}-${d}`
}

const prevMonth = () => {
  if (currentMonth.value === 0) { currentMonth.value = 11; currentYear.value-- }
  else currentMonth.value--
}
const nextMonth = () => {
  if (currentMonth.value === 11) { currentMonth.value = 0; currentYear.value++ }
  else currentMonth.value++
}

const schedules = ref([]);

const selectedCell = ref({ userId: null, day: null })
const showPopup = ref(false)

const onCellClick = (userId, day) => {
  if (selectedCell.value.userId === userId && selectedCell.value.day === day) {
    showPopup.value = !showPopup.value
  } else {
    selectedCell.value = { userId, day }
    showPopup.value = true
  }
}

const schedulesForDay = (userId, day) => {
  const dateStr = formatDate(currentYear.value, currentMonth.value, day)
  return schedules.value.filter(s => s.user === userId && s.date === dateStr)
}

const selectedSchedules = computed(() => {
  if (!showPopup.value || selectedCell.value.userId === null) return []
  return schedulesForDay(selectedCell.value.userId, selectedCell.value.day)
})

const statusClasses = (status) => {
  switch (status) {
    case 'TT': return 'bg-blue-500 text-white'
    case 'R': return 'bg-green-500 text-white'
    case 'MI': return 'bg-yellow-400 text-black'
    case 'P': return 'bg-red-500 text-white'
    case 'CM': return 'bg-purple-400 text-white'
    case 'M': return 'bg-gray-500 text-white'
    case 'F': return 'bg-indigo-400 text-white'
    case 'REC': return 'bg-pink-400 text-white'
    case 'SS': return 'bg-teal-400 text-white'
    default: return 'bg-gray-200 text-black'
  }
}

const getDayName = (day) => {
  const date = new Date(currentYear.value, currentMonth.value, day);
  return weekDays[date.getDay()].substring(0, 2);
};

// Helper pour détecter les weekends
const isWeekend = (day) => {
  const date = new Date(currentYear.value, currentMonth.value, day);
  const dayOfWeek = date.getDay();
  return dayOfWeek === 0 || dayOfWeek === 6; // 0 = Dimanche, 6 = Samedi
};

const isToday = (day) => {
  const now = new Date()
  return day === now.getDate() && 
         currentMonth.value === now.getMonth() && 
         currentYear.value === now.getFullYear()
}

const goToToday = () => {
  const today = new Date();
  currentMonth.value = today.getMonth(); // 0-11
  currentYear.value = today.getFullYear();  
};

onMounted(async () => {
  if (todayCell.value) {
    todayCell.value.scrollIntoView({
      behavior: 'smooth',
      inline: 'center', 
      block: 'nearest'
    })
  }

  try {
    schedules.value = await getAllSchedules() // récupère les données dynamiques
    users.value = await getAllUsers()
  } catch (error) {
    console.error('Erreur récupération schedules:', error)
  }
})
</script>
<template>
  <MainLayout>
    <div class="p-8 bg-gray-50 h-min-screen">
      <div class="max-w-7xl mx-auto bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">

        <div
          class="flex items-center justify-between p-5 border-b border-gray-100 bg-white/80 backdrop-blur-md sticky top-0">
          <div class="flex items-center gap-6">

            <div class="w-60 md:w-72 shrink-0">
              <h2 class="text-2xl font-extrabold text-gray-900 tracking-tight truncate">
                {{ monthNames[currentMonth] }}
                <span class="text-blue-500 font-light ml-1">{{ currentYear }}</span>
              </h2>
            </div>

            <div class="flex items-center bg-gray-100/80 rounded-2xl p-1.5 shadow-inner border border-gray-200/50">
              <button @click="prevMonth"
                class="p-2 hover:bg-white hover:shadow-md hover:text-blue-600 rounded-xl transition-all text-gray-500 active:scale-90">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" />
                </svg>
              </button>

              <div class="w-px h-5 bg-gray-300/60 mx-1.5"></div>

              <button @click="nextMonth"
                class="p-2 hover:bg-white hover:shadow-md hover:text-blue-600 rounded-xl transition-all text-gray-500 active:scale-90">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>

          <button @click="goToToday"
            class="hidden sm:block px-4 py-2 text-sm font-bold text-blue-600 hover:bg-blue-50 rounded-xl transition-colors">
            Aujourd'hui
          </button>
        </div>

        <div class="overflow-x-auto scroll-smooth">
          <table class="w-full border-separate border-spacing-0">
            <thead>
              <tr class="bg-gray-50/50">
                <th
                  class="sticky left-0 bg-white border-b border-r border-gray-200 px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-widest">
                  Collaborateurs
                </th>
                <th v-for="day in daysInMonth" :key="day" :ref="el => { if (isToday(day)) todayCell = el }" :class="[
                  'border-b border-gray-200 px-2 py-3 min-w-17.5 text-center transition-colors',
                  isWeekend(day) ? 'bg-gray-100/50' : ''
                ]">
                  <span :class="['block text-sm font-black', isWeekend(day) ? 'text-gray-400' : 'text-gray-800']">{{ day
                  }}</span>
                  <span class="text-[10px] uppercase font-bold text-gray-400">
                    {{ getDayName(day) }}
                  </span>
                </th>
              </tr>
            </thead>

            <tbody class="divide-y divide-gray-100">
              <tr v-for="user in users" :key="user.id" class="group transition-colors">
                <td
                  class="sticky left-0 bg-white group-hover:bg-indigo-50/30 border-r border-gray-100 px-6 py-4 whitespace-nowrap shadow-[4px_0_10px_-5px_rgba(0,0,0,0.05)] z-20">
                  <div class="flex items-center gap-4">
                    <div class="relative">
                      <div
                        class="w-10 h-10 rounded-xl bg-linear-to-br from-indigo-500 to-purple-600 text-white flex items-center justify-center text-xs font-bold shadow-md transform group-hover:scale-110 transition-transform">
                        {{ user.first_name[0] }}{{ user.last_name[0] }}
                      </div>
                    </div>
                    <div class="flex flex-col">
                      <span class="text-sm font-bold text-gray-800">{{ user.first_name }}</span>
                      <span class="text-[10px] text-gray-400 font-medium italic truncate w-24">{{ user.role_label
                      }}</span>
                    </div>
                  </div>
                </td>

                <td v-for="day in daysInMonth" :key="day" @click="onCellClick(user.id, day)" :class="[
                  'border-r border-gray-50 p-1.5 relative min-w-17.5 h-20 transition-all cursor-pointer',
                  isWeekend(day) ? 'bg-gray-50/50' : 'hover:bg-indigo-50/70'
                ]">

                  <div class="flex flex-col gap-1.5 h-full">
                    <div v-for="s in schedulesForDay(user.id, day)" :key="s.id"
                      class="text-[9px] leading-tight rounded-lg px-2 py-1.5 shadow-sm font-bold border-l-4 transition-transform hover:scale-105"
                      :class="statusClasses(s.status)">
                      {{ s.status_label }}
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <Transition name="fade">
        <div v-if="showPopup" class="fixed inset-0 flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-gray-900/10 backdrop-blur-[2px]" @click="showPopup = false"></div>

          <div class="relative bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden animate-slide-up">
            <div class="p-8">
              <div class="flex justify-between items-center mb-6">
                <div>
                  <p class="text-indigo-500 text-xs font-black uppercase tracking-widest">Détails du jour</p>
                  <h3 class="text-2xl font-bold text-gray-900">
                    {{ selectedCell.day }} {{ monthNames[currentMonth] }}
                  </h3>
                </div>
                <button @click="showPopup = false"
                  class="bg-gray-100 p-2 rounded-full text-gray-400 hover:text-gray-600 hover:rotate-90 transition-all">✕</button>
              </div>

              <div class="space-y-4 max-h-100 overflow-y-auto pr-2">
                <div v-for="s in selectedSchedules" :key="s.id"
                  class="group flex items-start gap-4 p-4 rounded-2xl bg-gray-50 border border-gray-100 hover:border-indigo-200 transition-colors">
                  <div :class="statusClasses(s.status)"
                    class="w-3 h-3 mt-1.5 rounded-full ring-4 ring-white shadow-sm shrink-0"></div>
                  <div class="flex-1">
                    <div class="flex justify-between">
                      <p class="text-[10px] font-black uppercase text-gray-400">{{ s.status_label }}</p>
                      <span class="text-[10px] text-gray-400">09:00 - 18:00</span>
                    </div>
                    <p class="text-sm font-medium text-gray-700 mt-1 leading-relaxed">{{ s.description }}</p>
                  </div>
                </div>

                <div v-if="selectedSchedules.length === 0" class="text-center py-10">
                  <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl">
                    ☕</div>
                  <p class="text-gray-400 text-sm font-medium">Rien de prévu pour cette journée.</p>
                </div>
              </div>

              <button @click="showPopup = false"
                class="w-full mt-8 py-4 bg-gray-900 text-white rounded-2xl font-bold hover:bg-indigo-600 hover:shadow-lg hover:shadow-indigo-200 transition-all active:scale-95">
                Fermer l'aperçu
              </button>
            </div>
          </div>
        </div>
      </Transition>

    </div>
  </MainLayout>
</template>
<style scoped>
.animate-slide-up {
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>