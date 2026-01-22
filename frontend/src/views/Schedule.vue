<script setup>
import { ref } from 'vue';
import MainLayout from '../layouts/MainLayout.vue';
import { getInitials } from '../utils/Methods';
import ScheduleDayView from '../components/schedule/ScheduleDayView.vue';

const userSelected = ref('all')
const viewOptionSelected = ref('dayView')
const isOpen = ref(false)

const viewOptions = [
  { valueOption: 'dayView', label: 'Vue du jour' },
  { valueOption: 'monthView', label: 'Vue du mois' },
  { valueOption: 'yearView', label: "Vue de l'année" }
]

const selectedLabel = () => viewOptions.find(o => o.valueOption === viewOptionSelected.value)?.label



const users = ref([
  {
    username: "tendrysteeve",
    first_name: "Tendry",
    last_name: "RASOLOMANDIMBY",
    email: "rasolomandimbytendry@gmail.com",
    role: "ADMIN",
    role_label: "Administrateur"
  },

  {
    username: "steeve",
    first_name: "Steeve",
    last_name: "RASOLOMANDIMBY",
    email: "rasolomandimbysteeve@gmail.com",
    role: "RESP",
    role_label: "Responsable"
  },

  {
    username: "antenaina",
    first_name: "Antenaina",
    last_name: "RASOLOMANDIMBY",
    email: "rasolomandimbyantenaina@gmail.com",
    role: "EMPLOYEE",
    role_label: "Employé"
  },
])


const getColorRole = (role) => {
  switch (role) {
    case 'ADMIN':
      return 'bg-fuchsia-50 text-fuchsia-500'
    case 'RESP':
      return 'bg-rose-50 text-rose-500'
    case 'EMPLOYEE':
      return 'bg-emerald-50 text-emerald-500'

    default:
      return ''

  }
}

</script>

<template>
  <MainLayout>
    <div class="grid grid-cols-4 gap-5 p-5">
      <div class="bg-white rounded-lg shadow-md p-5">
        <h3 class="text-indigo-500 text-2xl font-bold text-center py-3 mb-5">Voir les plannings</h3>
        <ul class="flex flex-col gap-5 m-h-160 overflow-y-auto py-5">
          <li>
            <button @click="userSelected = 'all'"
              :class="['w-full transition duration-200 py-4 px-5 rounded-xl text-start font-medium text-gray-600 text-lg', userSelected === 'all' ? 'bg-indigo-50 text-indigo-500' : 'hover:bg-indigo-50 bg-gray-50']">
              Tout le planning
            </button>
          </li>
          <li v-for="user in users" class="">
            <button @click="userSelected = user.username"
              :class="['w-full transition-all duration-150 py-2 px-3 rounded-md text-start border-l-5',
                userSelected === user.username ? 'border-indigo-500 shadow-sm' : 'hover:border-indigo-500 border-indigo-500/0 hover:shadow-2xl/5']">
              <div class="flex items-center gap-2">
                <span
                  class="w-8 h-8 flex items-center justify-center rounded-full bg-linear-30 from-sky-500 to-indigo-500 text-white text-sm font-bold">
                  {{ getInitials(user.first_name, user.last_name) }}
                </span>
                <div class="flex flex-col">
                  <span class="font-semibold text-gray-600 text-sm">{{ user.username }}</span>
                  <span :class="['px-2 py-1 text-xs rounded-full', getColorRole(user.role)]">{{ user.role_label
                  }}</span>
                </div>
              </div>
            </button>
          </li>
        </ul>
      </div>
      <div class="col-span-3 bg-white rounded-lg shadow-md">
        <!-- <div>
          <div class="flex justify-between items-center p-5 bg-indigo-50 rounded-t-lg">
            <span class="text-2xl font-bold text-gray-500">22 Janvier 2022</span>
            <div class="flex gap-3">
              <button class="px-4 py-2 rounded bg-white hover:bg-white/75 transition text-sm shadow-sm">Aujourd'hui</button>
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
              <button class="px-4 py-2 bg-blue-500 text-white font-medium rounded-lg text-sm hover:bg-blue-600 transition">Ajouter un
                événement</button>
            </div>
          </div>
        </div> -->
        <ScheduleDayView />
      </div>
    </div>
  </MainLayout>
</template>

<style scoped>
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: #94a3b8 #f1f5f9;
}

.overflow-y-auto::-webkit-scrollbar {
  height: 10px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 8px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: #94a3b8;
  border-radius: 8px;
  border: 2px solid #f1f5f9;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background-color: #64748b;
}
</style>
