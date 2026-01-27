<script setup>
import { computed, onMounted, ref } from 'vue'
import MainLayout from '../layouts/MainLayout.vue'
import { getAllLeaveForUser, createLeave, deleteLeave, editLeave } from '../api/leave'
import { profil } from '../api/auth'

import {
  CalendarDaysIcon,
  PlusIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  TrashIcon,
  XMarkIcon,
  PencilSquareIcon
} from '@heroicons/vue/24/outline'
import { BriefcaseIcon, CalendarIcon, ChatBubbleBottomCenterTextIcon, ChevronDownIcon, PaperAirplaneIcon } from '@heroicons/vue/24/solid'

const leaves = ref([])
const loading = ref(true)
const showModal = ref(false)
const submitting = ref(false)
const user = ref({})
const isEditMode = ref(false)
const editingId = ref(null)
const selectedStatus = ref('ALL')

const form = ref({
  leave_type: '',
  start_date: '',
  end_date: '',
  reason: ''
})

const loadLeaves = async () => {
  leaves.value = await getAllLeaveForUser()
  loading.value = false
}

const submitLeave = async () => {
  const payload = {
    ...form.value,
    user: user.value.id
  };

  submitting.value = true
  try {
    if (isEditMode.value) {
      await editLeave({ id: editingId.value, ...payload })
    } else {
      await createLeave(payload)
    }

    await loadLeaves()
    closeModal()
  } catch (error) {
    console.error("Erreur lors de l'enregistrement du congé :", error)
  } finally {
    submitting.value = false
  }
}

const closeModal = () => {
  showModal.value = false
  isEditMode.value = false
  editingId.value = null
  form.value = { leave_type: '', start_date: '', end_date: '', reason: '' }
}

const openEditModal = (leave) => {
  isEditMode.value = true
  editingId.value = leave.id
  form.value = {
    leave_type: leave.leave_type,
    start_date: leave.start_date,
    end_date: leave.end_date,
    reason: leave.reason
  }
  showModal.value = true
}

const removeLeave = async (id) => {
  if (!confirm('Supprimer ce congé ?')) return
  await deleteLeave(id)
  leaves.value = leaves.value.filter(l => l.id !== id)
}


const STATUS_MAP = {
  PENDING: { label: 'En attente', color: 'bg-yellow-500 text-yellow-700 ring-yellow-600/20', icon: ClockIcon },
  APPROVED: { label: 'Approuvé', color: 'bg-green-500 text-green-700 ring-green-600/20', icon: CheckCircleIcon },
  REJECTED: { label: 'Rejeté', color: 'bg-red-500 text-red-700 ring-red-600/20', icon: XCircleIcon },
}

// Filtrage corrigé
const filteredLeaves = computed(() => {
  if (selectedStatus.value === 'ALL') return leaves.value
  return leaves.value.filter(l => l.status?.toUpperCase() === selectedStatus.value.toUpperCase())
})

const getCount = (status) => {
  if (status === 'ALL') return leaves.value.length
  return leaves.value.filter(l => l.status?.toUpperCase() === status.toUpperCase()).length
}

const statusColor = (status) =>
  status === 'APPROVED' ? 'text-green-600' :
    status === 'REJECTED' ? 'text-red-600' :
      'text-yellow-600'

onMounted(async () => {
  await loadLeaves()
  try {
    user.value = await profil()
  } catch (e) {
    console.warn('Impossible de charger le profil')
  }
})
</script>

<template>
  <MainLayout>
    <div class="max-w-5xl mx-auto px-6 py-10 bg-gray-50/50">

      <div
        class="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10 p-4 rounded-2xl bg-white/50 backdrop-blur-sm border border-gray-100 shadow-sm">
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
              Mon congé
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

        <button @click="showModal = true"
          class="group relative overflow-hidden flex items-center justify-center gap-3 px-8 py-4 text-white font-bold rounded-2xl shadow-2xl transition-all duration-300 bg-blue-600 hover:-translate-y-1 active:scale-95">

          <div
            class="absolute inset-0 w-full h-full bg-linear-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]">
          </div>

          <div class="p-1 bg-white/20 rounded-lg group-hover:bg-white/30 transition-colors">
            <PlusIcon class="w-5 h-5 transition-transform duration-500 group-hover:rotate-90" />
          </div>

          <span class="tracking-wide">Nouvelle demande</span>
        </button>
      </div>

      <div class="flex items-center gap-3 mb-10 overflow-x-auto pb-4 scrollbar-hide">
        <button @click="selectedStatus = 'ALL'" :class="[
          selectedStatus === 'ALL'
            ? 'bg-white border-white shadow-xl shadow-blue-100/50 -translate-y-0.5'
            : 'bg-transparent border-transparent text-gray-400 hover:text-gray-600',
          'group relative px-6 py-3 rounded-2xl text-[11px] font-black border transition-all duration-300 whitespace-nowrap uppercase tracking-widest flex items-center gap-3'
        ]">
          <span>Tous</span>
          <span :class="[
            selectedStatus === 'ALL' ? 'bg-gray-300/20 ' : 'bg-gray-100 text-gray-500',
            'px-2 py-0.5 rounded-lg text-[10px] transition-colors font-bold'
          ]">
            {{ getCount('ALL') }}
          </span>
        </button>

        <div class="h-6 w-px bg-gray-200 mx-1"></div>

        <button v-for="(config, key) in STATUS_MAP" :key="key" @click="selectedStatus = key" :class="[
          selectedStatus === key
            ? 'bg-white border-white shadow-xl shadow-blue-100/50 -translate-y-0.5'
            : 'bg-transparent border-transparent text-gray-400 hover:text-gray-600',
          'group relative px-6 py-3 rounded-2xl text-[11px] font-black border transition-all duration-300 whitespace-nowrap uppercase tracking-widest flex items-center gap-3'
        ]">

          <div class="relative flex items-center justify-center">
            <span :class="[config.color, 'w-2 h-2 rounded-full relative z-10']"></span>
            <span v-if="selectedStatus === key"
              :class="[config.color, 'absolute inset-0 w-2 h-2 rounded-full animate-ping opacity-40']"></span>
          </div>

          {{ config.label }}

          <span :class="[
            selectedStatus === key ? 'bg-blue-50 text-blue-600' : 'bg-gray-100 text-gray-400 group-hover:bg-gray-200',
            'px-2 py-0.5 rounded-lg text-[10px] transition-all font-bold'
          ]">
            {{ getCount(key) }}
          </span>

          <div v-if="selectedStatus === key"
            class="absolute -bottom-1 left-1/2 -translate-x-1/2 w-8 h-1 bg-blue-500 rounded-full animate-in slide-in-from-bottom-1 duration-300">
          </div>
        </button>
      </div>

      <div class="relative">
        <Transition name="fade-slide" mode="out-in">
          <div v-if="filteredLeaves.length > 0" class="space-y-4" key="list">
            <TransitionGroup name="list">
              <div v-for="leave in filteredLeaves" :key="leave.id"
                class="group bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-xl hover:-translate-y-1 transition-all duration-300">

                <div class="flex">
                  <div
                    :class="[STATUS_MAP[leave.status]?.color || 'bg-gray-200', 'w-1.5 transition-colors duration-500']">
                  </div>

                  <div class="flex-1 p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">

                    <div class="flex-1 space-y-3">
                      <div class="flex items-center gap-3">
                        <div
                          class="flex items-center gap-2 bg-blue-50 text-blue-700 px-3 py-1.5 rounded-xl border border-blue-100 shadow-sm shadow-blue-50/50">
                          <CalendarIcon class="w-4 h-4 text-blue-500" />
                          <div class="flex items-center gap-1.5 text-[12px] font-black tracking-tight">
                            <span>{{ leave.start_date }}</span>
                            <span class="text-blue-300 font-normal">→</span>
                            <span>{{ leave.end_date }}</span>
                          </div>
                        </div>

                        <div :class="[
                          STATUS_MAP[leave.status]?.bg || 'bg-gray-50',
                          STATUS_MAP[leave.status]?.text || 'text-gray-500',
                          'flex items-center gap-2 px-3 py-1.5 rounded-full ring-1 ring-inset ring-black/3'
                        ]">
                          <span
                            :class="[STATUS_MAP[leave.status]?.color || 'bg-gray-400', 'w-1.5 h-1.5 rounded-full animate-pulse']"></span>
                          <span class="text-[10px] font-black uppercase tracking-widest">
                            {{ leave.status_label }}
                          </span>
                        </div>
                      </div>

                      <div class="space-y-1">
                        <h3 class="text-sm font-bold text-gray-900 ml-1">{{ leave.leave_type_label }}</h3>
                        <div
                          class="relative pl-4 border-l-2 border-gray-100 group-hover:border-blue-400 transition-colors duration-500">
                          <p class="text-gray-600 text-sm leading-relaxed font-medium">
                            {{ leave.reason || 'Aucun motif précisé' }}
                          </p>
                        </div>
                      </div>
                    </div>

                    <div
                      class="flex items-center gap-2 opacity-100 md:opacity-0 group-hover:opacity-100 transition-all duration-300 transform md:translate-x-4 group-hover:translate-x-0 w-full md:w-auto justify-end">
                      <button @click="openEditModal(leave)"
                        class="p-2.5 text-blue-600 bg-blue-50 hover:bg-blue-600 hover:text-white rounded-xl transition-all shadow-sm">
                        <PencilSquareIcon class="w-5 h-5" />
                      </button>
                      <button @click="removeLeave(leave.id)"
                        class="p-2.5 text-red-600 bg-red-50 hover:bg-red-600 hover:text-white rounded-xl transition-all shadow-sm">
                        <TrashIcon class="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </TransitionGroup>
          </div>

          <div v-else-if="leaves.length === 0"
            class="text-center py-20 bg-white rounded-[2.5rem] border-2 border-dashed border-gray-200" key="no-data">
            <div class="text-5xl mb-4">📝</div>
            <h3 class="text-xl font-bold text-gray-800">Aucune demande</h3>
            <button @click="showModal = true"
              class="mt-4 text-blue-600 font-bold hover:text-blue-800 transition-colors">
              Faire ma première demande
            </button>
          </div>

          <div v-else class="text-center py-20 bg-white rounded-[2.5rem] border-2 border-dashed border-gray-200"
            key="no-result">
            <div class="text-5xl mb-4 animate-bounce-slow">🔍</div>
            <h3 class="text-xl font-bold text-gray-800">Aucun résultat</h3>
            <p class="text-gray-400">Essayez de modifier vos filtres.</p>
            <button @click="selectedStatus = 'ALL'"
              class="mt-4 text-blue-600 font-bold hover:text-blue-800 transition-colors">
              Réinitialiser les filtres
            </button>
          </div>
        </Transition>
      </div>

      <Transition name="modal">
        <div v-if="showModal" @click.self="closeModal"
          class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/10 backdrop-blur-xs">

          <div
            class="bg-white rounded-[2.5rem] shadow-2xl w-full max-w-md overflow-hidden animate-in zoom-in-95 duration-300">

            <div class="relative p-8 pb-0">
              <div class="flex items-center justify-between mb-2">
                <span
                  class="px-3 py-1 bg-blue-100 text-blue-700 text-[10px] font-black uppercase tracking-widest rounded-full">
                  {{ isEditMode ? 'Édition' : 'Nouvelle Demande' }}
                </span>
                <button @click="closeModal" class="p-2 hover:bg-gray-100 rounded-full transition-colors group">
                  <XMarkIcon class="w-6 h-6 text-gray-400 group-hover:rotate-90 transition-transform" />
                </button>
              </div>
              <h2 class="text-3xl font-black text-gray-900 tracking-tight">
                {{ isEditMode ? 'Modifier le congé' : 'Demander un congé' }}
              </h2>
              <p class="text-gray-500 text-sm mt-1 font-medium">Précisez vos dates et le motif de votre absence.</p>
            </div>

            <div class="p-8 space-y-5">

              <div class="group">
                <label
                  class="flex items-center gap-2 text-xs font-bold uppercase text-gray-400 mb-2 ml-1 transition-colors group-focus-within:text-blue-600">
                  <BriefcaseIcon class="w-3.5 h-3.5" /> Type de congé
                </label>
                <div class="relative">
                  <select v-model="form.leave_type"
                    class="w-full p-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-blue-500 focus:ring-0 transition-all outline-none appearance-none text-gray-700 font-bold">
                    <option value="" disabled>Choisir un type...</option>
                    <option value="AN">Congé annuel</option>
                    <option value="ML">Maladie</option>
                    <option value="SP">Sans solde</option>
                    <option value="AU">Autorisation spéciale</option>
                  </select>
                  <ChevronDownIcon
                    class="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
                </div>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div class="group">
                  <label
                    class="flex items-center gap-2 text-xs font-bold uppercase text-gray-400 mb-2 ml-1 transition-colors group-focus-within:text-blue-600">
                    <CalendarIcon class="w-3.5 h-3.5" /> Début
                  </label>
                  <input type="date" v-model="form.start_date"
                    class="w-full p-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-blue-500 focus:ring-0 transition-all outline-none font-bold text-gray-700" />
                </div>
                <div class="group">
                  <label
                    class="flex items-center gap-2 text-xs font-bold uppercase text-gray-400 mb-2 ml-1 transition-colors group-focus-within:text-blue-600">
                    <CalendarIcon class="w-3.5 h-3.5" /> Fin
                  </label>
                  <input type="date" v-model="form.end_date"
                    class="w-full p-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-blue-500 focus:ring-0 transition-all outline-none font-bold text-gray-700" />
                </div>
              </div>

              <div class="group">
                <label
                  class="flex items-center gap-2 text-xs font-bold uppercase text-gray-400 mb-2 ml-1 transition-colors group-focus-within:text-blue-600">
                  <ChatBubbleBottomCenterTextIcon class="w-3.5 h-3.5" /> Motif ou détails
                </label>
                <textarea v-model="form.reason" rows="3" placeholder="Pourquoi ce congé ?"
                  class="w-full p-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-blue-500 focus:ring-0 transition-all outline-none resize-none font-medium text-gray-700"></textarea>
              </div>

              <div class="flex items-center gap-4 pt-4">
                <button @click="closeModal"
                  class="flex-1 py-4 font-bold text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-2xl transition-all">
                  Annuler
                </button>

                <button @click="submitLeave" :disabled="submitting"
                  class="flex-2 relative overflow-hidden group py-4 bg-blue-600 text-white rounded-2xl font-black shadow-xl shadow-blue-100 hover:bg-blue-700 active:scale-95 transition-all disabled:opacity-50">

                  <div
                    class="absolute inset-0 w-full h-full bg-linear-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]">
                  </div>

                  <span v-if="!submitting" class="flex items-center justify-center gap-2">
                    <PaperAirplaneIcon class="w-5 h-5 -rotate-45" /> Envoyer la demande
                  </span>

                  <span v-else class="flex items-center justify-center">
                    <svg class="animate-spin h-6 w-6 text-white" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                      </path>
                    </svg>
                  </span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>

    </div>
  </MainLayout>
</template>
<style scoped>
/* Transition pour la liste (v-for) */
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

/* Transition pour la Modal */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>