<script setup>
import { computed, onMounted, ref } from 'vue';
import MainLayout from '../layouts/MainLayout.vue';
import { createSchedule, deleteSchedule, editSchedule, getAllScheduleForUser } from '../api/schedule';
import { profil } from '../api/auth';
import { CalendarDaysIcon, PlusIcon, TrashIcon, PencilSquareIcon, CheckIcon, DocumentTextIcon, ChevronDownIcon, TagIcon, CalendarIcon } from '@heroicons/vue/24/solid';
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

      <div
        class="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10 p-5 rounded-2xl bg-white/60 backdrop-blur-md border border-gray-100 shadow-sm transition-all hover:shadow-md">

        <div class="flex items-center gap-4">
          <div class="relative group">
            <div class="absolute inset-0 bg-blue-500 blur-xl opacity-20 group-hover:opacity-40 transition-opacity">
            </div>

            <div
              class="relative p-3 bg-linear-to-br from-blue-600 to-indigo-700 rounded-2xl shadow-xl transform group-hover:rotate-6 transition-transform duration-300">
              <CalendarDaysIcon class="w-7 h-7 text-white" />
            </div>
          </div>

          <div>
            <h1 class="text-3xl font-black text-gray-900 tracking-tight leading-tight">
              Mon planning
            </h1>
            <div class="flex items-center gap-2 mt-1">
              <span class="relative flex h-2 w-2">
                <span
                  class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
              </span>
              <p class="text-xs font-bold text-blue-600/80 uppercase tracking-widest"></p>
            </div>
          </div>
        </div>

        <button @click="openAddModal"
          class="group relative overflow-hidden flex items-center justify-center gap-3 px-8 py-4 bg-blue-600 text-white font-bold rounded-2xl shadow-2xl transition-all duration-300 hover:-translate-y-1 active:scale-95">

          <div
            class="absolute inset-0 w-full h-full bg-linear-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]">
          </div>

          <div class="p-1 bg-white/20 rounded-lg group-hover:bg-white/30 transition-colors">
            <PlusIcon class="w-5 h-5 transition-transform duration-500 group-hover:rotate-90" />
          </div>

          <span class="tracking-wide">Nouvel événement</span>
        </button>
      </div>


      <div
        class="bg-white/60 backdrop-blur-md p-6 rounded-4xl shadow-sm border border-gray-100 mb-8 space-y-6 transition-all hover:shadow-md">

        <div class="relative group">
          <div
            class="absolute inset-0 bg-blue-500 blur-xl opacity-0 group-focus-within:opacity-10 transition-opacity duration-500">
          </div>

          <div class="relative flex items-center">
            <div class="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none">
              <MagnifyingGlassIcon
                class="h-5 w-5 text-gray-400 group-focus-within:text-blue-500 group-focus-within:scale-110 transition-all duration-300" />
            </div>

            <input type="text" v-model="searchQuery" placeholder="Rechercher une description..."
              class="block w-full pl-12 pr-12 py-4 bg-gray-50/50 border-2 border-transparent rounded-2xl text-sm font-medium focus:bg-white focus:border-blue-500 focus:ring-0 outline-none transition-all duration-300 placeholder:text-gray-400" />

            <Transition enter-active-class="duration-200 ease-out" enter-from-class="opacity-0 scale-95"
              enter-to-class="opacity-100 scale-100" leave-active-class="duration-150 ease-in"
              leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
              <button v-if="searchQuery" @click="searchQuery = ''"
                class="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-blue-600 transition-colors">
                <div class="p-1 hover:bg-blue-50 rounded-lg">
                  <XMarkIcon class="h-5 w-5" />
                </div>
              </button>
            </Transition>
          </div>
        </div>

        <div class="flex items-center gap-3 overflow-x-auto pb-2 scrollbar-hide">

          <button @click="selectedStatusFilter = 'Tous'" :class="[
            selectedStatusFilter === 'Tous'
              ? 'bg-gray-500 text-white shadow-lg shadow-gray-200 -translate-y-0.5'
              : 'bg-white text-gray-400 hover:text-gray-600 hover:bg-gray-50 border-transparent',
            'group px-6 py-3 rounded-xl text-[11px] font-black border transition-all duration-300 whitespace-nowrap uppercase tracking-widest flex items-center gap-2'
          ]">
            <span>Tous</span>
          </button>

          <div class="h-6 w-px bg-gray-200 mx-1 shrink-0"></div>

          <button v-for="(config, key) in STATUS_CONFIG" :key="key" @click="selectedStatusFilter = config.label" :class="[
            selectedStatusFilter === config.label
              ? 'bg-white border-white shadow-xl shadow-blue-100/50 -translate-y-0.5'
              : 'bg-transparent border-transparent text-gray-400 hover:text-gray-600',
            'group relative px-5 py-3 rounded-xl text-[11px] font-black border transition-all duration-300 whitespace-nowrap uppercase tracking-widest flex items-center gap-3'
          ]">

            <div class="relative flex items-center justify-center">
              <span
                :class="[config.dot, 'w-2 h-2 rounded-full relative z-10 transition-transform duration-300', selectedStatusFilter === config.label ? 'scale-125' : '']"></span>
              <span v-if="selectedStatusFilter === config.label"
                :class="[config.dot, 'absolute inset-0 w-2 h-2 rounded-full animate-ping opacity-40']"></span>
            </div>

            {{ config.label }}

            <div v-if="selectedStatusFilter === config.label"
              class="absolute -bottom-1 left-1/2 -translate-x-1/2 w-6 h-1 bg-blue-500 rounded-full animate-in slide-in-from-bottom-1">
            </div>
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
          <div v-else-if="schedules.length === 0"
            class="text-center py-20 bg-white rounded-3xl border border-dashed border-gray-200" key="no-data">
            <h3 class="text-xl font-bold text-gray-800">Aucun évènement</h3>
            <button @click="openAddModal" class="mt-4 text-blue-600 font-bold hover:text-blue-800 transition-colors">
              Ajouter un évènement
            </button>
          </div>
          <div v-else class="text-center py-20 bg-white rounded-3xl border border-dashed border-gray-200"
            key="no-result">
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

        <div v-if="isModalOpen" @click.self="closeModal"
          class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/60 backdrop-blur-md">

          <div
            class="bg-white rounded-4xl shadow-2xl w-full max-w-md overflow-hidden animate-in zoom-in-95 duration-300">

            <div class="relative p-8 pb-0">
              <div class="flex items-center justify-between mb-2">
                <span
                  class="px-3 py-1 bg-blue-100 text-blue-700 text-[10px] font-black uppercase tracking-widest rounded-full">
                  {{ isEditMode ? 'Édition' : 'Nouveau' }}
                </span>
                <button @click="closeModal" class="p-2 hover:bg-gray-100 rounded-full transition-colors">
                  <XMarkIcon class="w-5 h-5 text-gray-400" />
                </button>
              </div>
              <h3 class="text-3xl font-black text-gray-900 tracking-tight">
                {{ isEditMode ? 'Modifier l\'événement' : 'Nouvel événement' }}
              </h3>
              <p class="text-gray-500 text-sm mt-1">Remplissez les détails ci-dessous.</p>
            </div>

            <form @submit.prevent="handleSubmit" class="p-8 space-y-5">

              <div class="group">
                <label
                  class="flex items-center gap-2 text-xs font-bold uppercase text-gray-400 mb-2 ml-1 transition-colors group-focus-within:text-blue-600">
                  <CalendarIcon class="w-3 h-3" /> Date de l'événement
                </label>
                <input type="date" v-model="formData.date" required
                  class="w-full p-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-blue-500 focus:ring-0 transition-all outline-none text-gray-700 font-medium" />
              </div>

              <div class="group">
                <label
                  class="flex items-center gap-2 text-xs font-bold uppercase text-gray-400 mb-2 ml-1 transition-colors group-focus-within:text-blue-600">
                  <TagIcon class="w-3 h-3" /> Catégorie / Statut
                </label>
                <div class="relative">
                  <select v-model="formData.status_label"
                    class="w-full p-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-blue-500 focus:ring-0 transition-all outline-none appearance-none text-gray-700 font-medium">
                    <option value="" disabled>Choisir un statut...</option>
                    <option v-for="config in STATUS_CONFIG" :key="config.label" :value="config.label">
                      {{ config.label }}
                    </option>
                  </select>
                  <ChevronDownIcon
                    class="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
                </div>
              </div>

              <div class="group">
                <label
                  class="flex items-center gap-2 text-xs font-bold uppercase text-gray-400 mb-2 ml-1 transition-colors group-focus-within:text-blue-600">
                  <DocumentTextIcon class="w-3 h-3" /> Notes complémentaires
                </label>
                <textarea v-model="formData.description" rows="3" placeholder="Ajoutez des détails..."
                  class="w-full p-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-blue-500 focus:ring-0 transition-all outline-none resize-none text-gray-700 font-medium"></textarea>
              </div>

              <div class="flex items-center gap-4 mt-8">
                <button type="button" @click="closeModal"
                  class="flex-1 py-4 font-bold text-gray-400 hover:text-gray-600 transition-colors">
                  Annuler
                </button>

                <button type="submit" :disabled="isLoading"
                  class="flex-2 relative overflow-hidden group py-4 bg-blue-600 text-white rounded-2xl font-bold shadow-xl shadow-blue-200 hover:bg-blue-700 active:scale-95 transition-all disabled:opacity-50">
                  <span v-if="!isLoading" class="flex items-center justify-center gap-2">
                    <CheckIcon class="w-5 h-5" /> Confirmer
                  </span>
                  <span v-else class="flex items-center justify-center">
                    <svg class="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                      </circle>
                      <path class="opacity-75" fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                      </path>
                    </svg>
                  </span>
                </button>
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