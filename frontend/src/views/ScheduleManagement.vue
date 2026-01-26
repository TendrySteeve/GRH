<script setup>
import { computed, onMounted, ref } from 'vue';
import MainLayout from '../layouts/MainLayout.vue';
import { createSchedule, deleteSchedule, editSchedule, getAllScheduleForUser } from '../api/schedule';
import { profil } from '../api/auth';
import { CalendarDaysIcon, PlusIcon, TrashIcon, PencilSquareIcon } from '@heroicons/vue/24/solid';
import { MagnifyingGlassIcon, XMarkIcon } from '@heroicons/vue/24/outline';

const schedules = ref([]);
const isModalOpen = ref(false);
const isEditMode = ref(false);
const user = ref({});
const searchQuery = ref('');
const selectedStatusFilter = ref('Tous');

const formData = ref({
  id: null,
  date: '',
  status_label: 'Sur site',
  description: ''
});

const STATUS_CONFIG = {
  TT: { label: 'Télétravail', color: 'bg-green-100', border: 'border-green-500', text: 'text-green-800', dot: 'bg-green-500' },
  R: { label: 'Réunion', color: 'bg-blue-100', border: 'border-blue-500', text: 'text-blue-800', dot: 'bg-blue-500' },
  CM: { label: 'Congé maternité', color: 'bg-pink-100', border: 'border-pink-500', text: 'text-pink-800', dot: 'bg-pink-500' },
  MI: { label: 'Mission', color: 'bg-yellow-100', border: 'border-yellow-500', text: 'text-yellow-800', dot: 'bg-yellow-500' },
  P: { label: 'Permission', color: 'bg-purple-100', border: 'border-purple-500', text: 'text-purple-800', dot: 'bg-purple-500' },
  M: { label: 'Maladie', color: 'bg-red-100', border: 'border-red-500', text: 'text-red-800', dot: 'bg-red-500' },
  F: { label: 'Formation', color: 'bg-indigo-100', border: 'border-indigo-500', text: 'text-indigo-800', dot: 'bg-indigo-500' },
  REC: { label: 'Récupération', color: 'bg-teal-100', border: 'border-teal-500', text: 'text-teal-800', dot: 'bg-teal-500' },
  SS: { label: 'Sur site', color: 'bg-gray-100', border: 'border-gray-400', text: 'text-gray-800', dot: 'bg-gray-400' }
};

const getStatusConfig = (statusLabel) => {
  const statusKey = Object.keys(STATUS_CONFIG).find(key => STATUS_CONFIG[key].label === statusLabel);
  return STATUS_CONFIG[statusKey] || STATUS_CONFIG.SS;
};

const getStatusKeyFromLabel = (label) => {
  return Object.keys(STATUS_CONFIG).find(key => STATUS_CONFIG[key].label === label) || 'SS';
};

const filteredSchedules = computed(() => {
  return schedules.value.filter(s => {
    const matchesStatus = selectedStatusFilter.value === 'Tous' || s.status_label === selectedStatusFilter.value;
    const searchLower = searchQuery.value.toLowerCase();
    const matchesSearch = (s.description?.toLowerCase().includes(searchLower)) || (s.status_label.toLowerCase().includes(searchLower));
    return matchesStatus && matchesSearch;
  }).sort((a, b) => new Date(b.date) - new Date(a.date)); // Tri par date décroissante
});

const resetForm = () => {
  formData.value = { id: null, date: '', status_label: 'Sur site', description: '' };
};

const openAddModal = () => {
  isEditMode.value = false;
  resetForm();
  isModalOpen.value = true;
};

const openEditModal = (schedule) => {
  isEditMode.value = true;
  formData.value = { ...schedule };
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  resetForm();
};

const handleSubmit = async () => {
  const payload = {
    ...formData.value,
    status: getStatusKeyFromLabel(formData.value.status_label),
    user: user.value.id
  };

  try {
    if (isEditMode.value) {
      await editSchedule(payload);
    } else {
      await createSchedule(payload);
    }
    schedules.value = await getAllScheduleForUser();
    closeModal();
  } catch (error) {
    console.error("Erreur lors de l'enregistrement", error);
  }
};

const handleDelete = async (id) => {
  try {
    await deleteSchedule(id);
    schedules.value = schedules.value.filter(s => s.id !== id);
  } catch (error) {
    console.error(error);
  }
};

onMounted(async () => {
  try {
    schedules.value = await getAllScheduleForUser();
    user.value = await profil();
  } catch (error) {
    console.log(error);
  }
});
</script>
<template>
  <MainLayout>
    <div class="max-w-5xl mx-auto px-6 py-10 bg-gray-50/50">

      <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8">
        <div>
          <div class="flex items-center gap-3 mb-2">
            <div class="p-2 bg-blue-600 rounded-lg shadow-lg shadow-blue-200">
              <CalendarDaysIcon class="w-6 h-6 text-white" />
            </div>
            <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">Mon Planning</h1>
          </div>
          <p class="text-gray-500 font-medium">Gérez vos présences et événements</p>
        </div>

        <button @click="openAddModal"
          class="flex items-center justify-center gap-2 px-6 py-3 bg-blue-700 hover:bg-blue-600 text-white font-bold rounded-xl shadow-lg transition-all duration-300 active:scale-95 hover:shadow-blue-200">
          <PlusIcon class="w-5 h-5" /> Nouvel événement
        </button>
      </div>

      <div class="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 mb-8 space-y-4">
        <div class="relative group">
          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <MagnifyingGlassIcon class="h-5 w-5 text-gray-400 group-focus-within:text-blue-500 transition-colors" />
          </div>
          <input type="text" v-model="searchQuery" placeholder="Rechercher une description..."
            class="block w-full pl-11 pr-10 py-3 bg-gray-50 border border-transparent rounded-xl text-sm focus:ring-4 focus:ring-blue-100 focus:bg-white focus:border-blue-200 outline-none transition-all duration-300" />

          <Transition name="fade">
            <button v-if="searchQuery" @click="searchQuery = ''"
              class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600">
              <XMarkIcon class="h-5 w-5" />
            </button>
          </Transition>
        </div>

        <div class="flex items-center gap-2 overflow-x-auto py-2 scrollbar-hid">
          <button @click="selectedStatusFilter = 'Tous'" :class="[
            selectedStatusFilter === 'Tous' ? 'bg-gray-400 text-white shadow-md' : 'bg-white text-gray-500 hover:bg-gray-100 border-gray-200',
            'px-4 py-2 rounded-lg text-xs font-bold border transition-all duration-200 whitespace-nowrap uppercase'
          ]">
            Tous
          </button>
          <button v-for="(config, key) in STATUS_CONFIG" :key="key" @click="selectedStatusFilter = config.label" :class="[
            selectedStatusFilter === config.label ? 'ring-2 ring-blue-500 bg-white border-blue-500 shadow-sm' : 'bg-white text-gray-500 border-gray-100 hover:bg-gray-50',
            'flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-bold border transition-all duration-200 whitespace-nowrap uppercase'
          ]">
            <span
              :class="[config.dot, 'w-2 h-2 rounded-full transition-transform duration-300', selectedStatusFilter === config.label ? 'scale-125' : '']"></span>
            {{ config.label }}
          </button>
        </div>
      </div>

      <div class="relative">
        <Transition name="fade-slide" mode="out-in">
          <div v-if="filteredSchedules.length > 0" class="grid grid-cols-1 gap-4" key="list">
            <TransitionGroup name="list">
              <div v-for="schedule in filteredSchedules" :key="schedule.id"
                class="group bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                <div class="flex">
                  <div :class="[getStatusConfig(schedule.status_label).dot, 'w-1.5 transition-colors duration-500']">
                  </div>

                  <div class="flex-1 p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div class="space-y-1">
                      <div class="flex items-center gap-3">
                        <span class="text-sm font-bold text-gray-900">{{ schedule.date }}</span>
                        <span :class="[
                          getStatusConfig(schedule.status_label).color,
                          getStatusConfig(schedule.status_label).text,
                          'px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider'
                        ]">
                          {{ schedule.status_label }}
                        </span>
                      </div>
                      <p class="text-gray-600 text-sm leading-relaxed">{{ schedule.description || 'Aucune description'
                        }}</p>
                    </div>

                    <div
                      class="flex items-center gap-2 opacity-100 md:opacity-0 group-hover:opacity-100 transition-all duration-300 transform group-hover:translate-x-0 md:translate-x-2">
                      <button @click="openEditModal(schedule)"
                        class="p-2 text-blue-600 bg-blue-50 hover:bg-blue-600 hover:text-white rounded-lg transition-all duration-200">
                        <PencilSquareIcon class="w-5 h-5" />
                      </button>
                      <button @click="handleDelete(schedule.id)"
                        class="p-2 text-red-600 bg-red-50 hover:bg-red-600 hover:text-white rounded-lg transition-all duration-200">
                        <TrashIcon class="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </TransitionGroup>
          </div>
          <div v-else-if="schedules.length === 0" class="text-center py-20 bg-white rounded-3xl border border-dashed border-gray-200" key="no-data">
            <h3 class="text-xl font-bold text-gray-800">Aucun évènement</h3>
            <button @click="openAddModal"
              class="mt-4 text-blue-600 font-bold hover:text-blue-800 transition-colors">
              Ajouter un évènement
            </button>
          </div>
          <div v-else class="text-center py-20 bg-white rounded-3xl border border-dashed border-gray-200" key="no-result">
            <div class="text-5xl mb-4 animate-bounce-slow">🔍</div>
            <h3 class="text-xl font-bold text-gray-800">Aucun résultat</h3>
            <p class="text-gray-400">Essayez de modifier vos filtres ou votre recherche.</p>
            <button @click="searchQuery = ''; selectedStatusFilter = 'Tous'"
              class="mt-4 text-blue-600 font-bold hover:text-blue-800 transition-colors">
              Réinitialiser les filtres
            </button>
          </div>
        </Transition>
      </div>

      <Transition name="modal">
        <div v-if="isModalOpen"
          class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
          <div class="bg-white rounded-3xl shadow-2xl w-full max-w-md p-8 animate-in zoom-in duration-200">
            <h3 class="text-2xl font-black text-gray-900 mb-6">{{ isEditMode ? 'Modifier' : 'Ajouter' }}</h3>
            <form @submit.prevent="handleSubmit" class="space-y-4">
              <div>
                <label class="block text-xs font-bold uppercase text-gray-400 mb-1">Date</label>
                <input type="date" v-model="formData.date" required
                  class="w-full p-3 bg-gray-50 border-none rounded-xl focus:ring-2 focus:ring-blue-500" />
              </div>
              <div>
                <label class="block text-xs font-bold uppercase text-gray-400 mb-1">Statut</label>
                <select v-model="formData.status_label"
                  class="w-full p-3 bg-gray-50 border-none rounded-xl focus:ring-2 focus:ring-blue-500">
                  <option v-for="config in STATUS_CONFIG" :key="config.label" :value="config.label">{{ config.label }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-bold uppercase text-gray-400 mb-1">Description</label>
                <textarea v-model="formData.description" rows="3"
                  class="w-full p-3 bg-gray-50 border-none rounded-xl focus:ring-2 focus:ring-blue-500 resize-none"></textarea>
              </div>
              <div class="flex gap-3 mt-6">
                <button type="button" @click="closeModal" class="flex-1 py-3 font-bold text-gray-500">Annuler</button>
                <button type="submit" class="flex-1 py-3 bg-blue-600 text-white rounded-xl font-bold">Confirmer</button>
              </div>
            </form>
          </div>
        </div>
      </Transition>

    </div>
  </MainLayout>
</template>

<style scoped>
/* 1. Animation de la liste (TransitionGroup) */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.list-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(100px);
}

/* Pour que les éléments restants glissent doucement à leur nouvelle place */
.list-move {
  transition: transform 0.5s ease;
}

/* 2. Transition Fade-Slide (entre liste et état vide) */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: scale(0.98);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: scale(1.02);
}

/* 3. Animation de la Modal */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-content {
  animation: modal-in 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-leave-active .modal-content {
  animation: modal-in 0.2s reverse ease-in;
}

@keyframes modal-in {
  0% {
    transform: scale(0.9) translateY(20px);
    opacity: 0;
  }

  100% {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
}

/* 4. Divers */
.animate-bounce-slow {
  animation: bounce 3s infinite;
}

@keyframes bounce {

  0%,
  100% {
    transform: translateY(-5%);
  }

  50% {
    transform: translateY(0);
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

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>