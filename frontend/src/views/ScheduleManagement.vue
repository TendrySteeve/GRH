<script setup>
import { onMounted, ref } from 'vue';
import MainLayout from '../layouts/MainLayout.vue';
import { createSchedule, deleteSchedule, editSchedule, getAllSchedule } from '../api/schedule';
import { profil } from '../api/auth';
import { CalendarDaysIcon } from '@heroicons/vue/24/solid';

const schedules = ref([])
const isModalOpen = ref(false)
const isEditMode = ref(false)
const user = ref({})
const formData = ref({
  id: null,
  date: '',
  status_label: 'Sur site',
  description: ''
})

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

const getStatusConfig = (statusLabel) => {
  const statusKey = Object.keys(STATUS_CONFIG).find(
    key => STATUS_CONFIG[key].label === statusLabel
  );
  return STATUS_CONFIG[statusKey] || STATUS_CONFIG.SS;
}

const getStatusKeyFromLabel = (label) => {
  return Object.keys(STATUS_CONFIG).find(key => STATUS_CONFIG[key].label === label) || 'SS';
}


const resetForm = () => {
  formData.value = {
    id: null,
    date: '',
    status_label: 'Sur site',
    description: ''
  }
}

const openAddModal = () => {
  isEditMode.value = false
  resetForm()
  isModalOpen.value = true
}

const openEditModal = (schedule) => {
  isEditMode.value = true
  formData.value = {
    id: schedule.id,
    date: schedule.date,
    status_label: schedule.status_label,
    description: schedule.description || ''
  }
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
  resetForm()
}

const handleSubmit = async () => {
  formData.value = {
    ...formData.value,
    status: getStatusKeyFromLabel(formData.value.status_label),
    user: user.value.id
  }

  let newSchedule

  try {
    if (isEditMode.value) {
      newSchedule = await editSchedule(formData.value)
      const index = schedules.value.findIndex(s => s.id === formData.value.id)
      if (index !== -1) schedules.value[index] = newSchedule
    } else {
      newSchedule = await createSchedule(formData.value)
      if (newSchedule) schedules.value.push(newSchedule)
    }
    const data = await getAllSchedule()
    schedules.value = data
    closeModal()
  } catch (error) {
    console.error(error)
  }
}

const handleDelete = async (scheduleId) => {

  try {
    const res = await deleteSchedule(scheduleId)
    schedules.value = schedules.value.filter(s => s.id !== scheduleId)
  } catch (error) {
    console.error(error)
  }

}

onMounted(async () => {
  try {
    schedules.value = await getAllSchedule();
    user.value = await profil();
  } catch (error) {
    console.log(error)
  }
})
</script>

<template>
  <MainLayout>
    <div class="max-w-4xl mx-auto px-4 py-8">
      <div class="mb-8 flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">Planning</h1>
          <p class="text-gray-600">Consultez votre emploi du temps</p>
        </div>
        <button @click="openAddModal"
          class="inline-flex items-center gap-2 px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg shadow-sm hover:shadow-md transition-all duration-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Ajouter
        </button>
      </div>

      <div v-if="schedules.length === 0"
        class="text-center py-12 bg-gray-50 rounded-xl border-2 border-dashed border-gray-300">
        <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <p class="text-gray-500 text-lg mb-4">Aucun événement planifié</p>
        <button @click="openAddModal"
          class="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-200">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Ajouter un événement
        </button>
      </div>

      <div v-else class="space-y-4">
        <div v-for="schedule in schedules"
          class="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 overflow-hidden border border-gray-200">
          <div class="p-6">
            <div class="flex items-start justify-between gap-4">
              <div class="flex gap-3">
                <div class="text-lg font-semibold text-gray-600 flex items-center gap-1">
                  <CalendarDaysIcon class="w-5 h-5" /> {{ schedule.date }}
                </div>
                <span :class="[
                  getStatusConfig(schedule.status_label).color,
                  getStatusConfig(schedule.status_label).text,
                  getStatusConfig(schedule.status_label).border,
                  'inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border-2'
                ]">
                  {{ schedule.status_label }}
                </span>
              </div>

              <div class="flex flex-col items-end gap-3">
                <div class="flex gap-2">
                  <button @click="openEditModal(schedule)"
                    class="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-blue-700 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors duration-200">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                    Modifier
                  </button>
                  <button @click="handleDelete(schedule.id)"
                    class="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-red-700 bg-red-50 hover:bg-red-100 rounded-lg transition-colors duration-200">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    Supprimer
                  </button>
                </div>
              </div>
            </div>

            <div v-if="schedule.description" class="mt-4 pt-4 border-t border-gray-100">
              <p class="text-gray-700 text-sm leading-relaxed">{{ schedule.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="isModalOpen" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog"
        aria-modal="true">
        <div
          class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0 bg-white/5 backdrop-blur-[2px]">
          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

          <div
            class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-2xl font-bold text-gray-900" id="modal-title">
                {{ isEditMode ? 'Modifier l\'événement' : 'Ajouter un événement' }}
              </h3>
              <button @click="closeModal" class="text-gray-400 hover:text-gray-600 transition-colors">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <form @submit.prevent="handleSubmit" class="space-y-5">
              <div>
                <label for="date" class="block text-sm font-medium text-gray-700 mb-2">
                  Date
                </label>
                <input type="date" id="date" v-model="formData.date" required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors" />
              </div>
              <div>
                <label for="status" class="block text-sm font-medium text-gray-700 mb-2">
                  Statut
                </label>
                <select id="status" v-model="formData.status_label" required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors">
                  <option v-for="(config, key) in STATUS_CONFIG" :key="key" :value="config.label">
                    {{ config.label }}
                  </option>
                </select>
              </div>

              <div>
                <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
                  Description (optionnel)
                </label>
                <textarea id="description" v-model="formData.description" rows="3"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors resize-none"
                  placeholder="Ajouter des détails..."></textarea>
              </div>

              <div class="flex gap-3 pt-4">
                <button type="button" @click="closeModal"
                  class="flex-1 px-4 py-2.5 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors">
                  Annuler
                </button>
                <button type="submit"
                  class="flex-1 px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors">
                  {{ isEditMode ? 'Enregistrer' : 'Ajouter' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>